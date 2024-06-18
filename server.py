import socket
import sys
import select

class GameStart(Exception): pass

HEADER_LENGTH = 10

if len(sys.argv) != 3:
    print("Argument format: server.py <IP address> <port>")
    exit()

IPaddr = str(sys.argv[1])
port = int(sys.argv[2])

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IPaddr, port))
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
            if sock==server_socket:
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
    except GameStart:
        break
                

# MULTICAST GROUP
MCAST_GROUP = '224.1.1.1'
MCAST_PORT = 5007
MCAST_TTL = 2
multicast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MCAST_TTL)


print("\n",clients,"\n")

starting_socket = sockets_list[1]
starting_socket.send("You start".encode())


turn = 0
while True: # game loop
    current_socket = sockets_list[(turn%2)+1]
    turn+=1

    message = current_socket.recv(2048)
    message = message.decode()
    # if message is False:
    #     print(f"Closed connection from {clients[current_socket]['data'].decode()}")
    #     sockets_list.remove(current_socket)
    #     del clients[current_socket]
    #     continue
    
    user = clients[current_socket]
    print(f"Received message from {user['data'].decode()}: {message}")
    for client in clients:
        if client != current_socket:
            client.send("Your turn".encode())

    
    # for sock in exception_sockets: # maybe to add somewhere later
    #     sockets_list.remove(sock)
    #     del clients[sock]
