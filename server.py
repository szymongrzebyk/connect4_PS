import socket
import sys
import select
import tlv8
from control import *
import errno
import random
import time


class GameStart(Exception): pass


HEADER_LENGTH = 10

if len(sys.argv) != 3:
    print("Argument format: server.py <IP address> <port>")
    exit()

addr = str(sys.argv[1])
port = int(sys.argv[2])

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

dns_list = socket.getaddrinfo(addr,port)
for s in dns_list:
    if s[0] is socket.AddressFamily.AF_INET and s[1] is socket.SocketKind.SOCK_STREAM:
        sockaddr = s[4]

server_socket.bind(sockaddr)
server_socket.listen(2)

sockets_list = [server_socket]

clients = {}


def recv_msg(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        if not len(message_header):
            return False
        
        message_length = int(message_header.decode('utf-8').strip())

        return {'header': message_header, 'data': client_socket.recv(message_length)}
    except:
        return False



while True:
    try:
        read_sockets, write_sockets, exception_sockets = select.select(sockets_list, [], sockets_list)
        
        for sock in read_sockets:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()

                user = recv_msg(client_socket)
                if user is False:
                    continue
                
                # if len(clients) == 2:
                #     client_socket.send("Game full".encode())
                #     client_socket.close()
                
                sockets_list.append(client_socket)

                clients[client_socket] = user

                print(f"Connection from {client_address[0]}:{client_address[1]}, user {user['data'].decode()}")
                client_socket.send("Successfully connected".encode())

                if len(clients) == 2:
                    raise GameStart
        
        # for sock in exception_sockets:
        #     sockets_list.remove(sock)
        #     del clients[sock]
    except GameStart:
        time.sleep(1)
        sockets_list[1].send('Log'.encode())
        sockets_list[2].send('Log'.encode())
        break
                

# MULTICAST GROUP
MCAST_GROUP = '224.1.1.1'
MCAST_PORT = 5007
MCAST_TTL = 2
multicast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MCAST_TTL)

client1_logged = False
client2_logged = False
client_usernames = []

while not client1_logged or not client2_logged:  # logging in loop
    for socket in range(1, len(sockets_list)):
        current_socket = sockets_list[socket]
        creds_struct = current_socket.recv(2048)
        if not creds_struct:
            continue
        expected_struct = {
            1: tlv8.DataType.STRING,
            2: tlv8.DataType.STRING
        }
        received_creds = tlv8.decode(creds_struct, expected_struct)
        creds_as_string = tlv8.format_string(received_creds)
        print(creds_as_string)
        user_login = received_creds[0].data
        user_hash = received_creds[1].data
        # received_creds_list = received_creds.split(':')  # expected format {login}:{hash}
        creds_file = open('creds.txt', 'r')
        user_exists = False
        for line in creds_file:
            single_user = line.strip().split(':')
            if single_user[0] == user_login:
                user_exists = True
                if single_user[1] == user_hash:
                    if client1_logged:
                        client2_logged = True
                        client_usernames.append(user_login)
                        print("client 2 logged")
                    else:
                        client1_logged = True
                        client_usernames.append(user_login)
                        print("client 1 logged")
                    current_socket.send('OK'.encode())
                else:
                    print("Wrong pass")
                    current_socket.send('WRONG PASS'.encode())
        creds_file.close()
        if not user_exists:
            creds_file = open('creds.txt', 'a')
            creds_file.write("\n" + user_login + ':' + user_hash)
            current_socket.send('OK'.encode())
creds_file.close()


# print("\n",clients,"\n")
print("start")
starting_socket = sockets_list[1]
starting_socket.send("You start".encode())

line = ""
log_file = open("games.log", "r+")
for line in log_file:
    pass
last_line = line
print(last_line)
if last_line == "":
    game_id = 0
else:
    last_game = last_line.strip().split(':')
    game_id = int(last_game[0]) + random.randint(1,20)

# log format: {id}:{current_player}:{opposite_player}:{move}

turn = 0
while True: # game loop
    current_socket = sockets_list[(turn%2)+1]
    

    message = current_socket.recv(2048)
    
    if not message:
        print(f"Closed connection from {clients[current_socket]['data'].decode()}")
        sockets_list.remove(current_socket)
        del clients[current_socket]
        for client in clients:
            if client != current_socket:
                client.send("Client disconnected".encode())
        multicast_socket.sendto("Client disconnected".encode(), (MCAST_GROUP, MCAST_PORT))
        break
    
    message_decoded = message.decode()
    
    user = clients[current_socket]
    print(f"Received message from {user['data'].decode()}: {message_decoded}")
    for client in clients:
        if client != current_socket:
            client.send(message)
    multicast_socket.sendto(message, (MCAST_GROUP, MCAST_PORT))
    log_file.write(str(game_id)+':'+client_usernames[turn%2]+':'+client_usernames[(turn+1)%2]+':'+str(message_decoded)+"\n")
    turn+=1

log_file.close()