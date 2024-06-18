import socket
import sys
import select

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

print(f'Listening for connections on {IPaddr}:{port}...')

def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        if not len(message_header):
            return False
        
        message_length = int(message_header.decode('utf-8').strip())

        return {'header': message_header, 'data': client_socket.recv(message_length)}
    except:
        return False
    
while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for sock in read_sockets:
        if sock==server_socket:
            client_socket, client_address = server_socket.accept()

            user = receive_message(client_socket)
            if user is False:
                continue
            
            if len(clients) == 2:
                client_socket.send("Game full".encode())
                client_socket.close()
            else:
                sockets_list.append(client_socket)

                clients[client_socket] = user

                print(f"Connection from {client_address[0]}:{client_address[1]}, user {user['data'].decode()}")
                client_socket.send("Successfully connected".encode())
        else:
            message = receive_message(sock)
            if message is False:
                print('Closed connection from: {}'.format(clients[sock]['data'].decode('utf-8')))
                sockets_list.remove(sock)
                del clients[sock]
                continue
            user = clients[sock]
            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

            for client_socket in clients:
                if client_socket != sock:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    for sock in exception_sockets:
        sockets_list.remove(sock)
        del clients[sock]