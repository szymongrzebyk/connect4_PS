import socket
import sys
import select

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
        message_header = client_socket.recv(10)

        if not len(message_header):
            return False
        
        message_lenght = int(message_header.decode().strip())
        return {"header": message_header, "data": client_socket.recv(message_lenght)}
    
    except:
        return False



while True:
    read_sockets, write_sockets, exception_sockets = select.select(sockets_list, [], sockets_list)

    for sock in read_sockets:
        if sock==server_socket:
            client_socket, client_address = server_socket.accept()

            user = recv_msg(client_socket)
            if user is False:
                continue

            sockets_list.append(client_socket)

            clients[client_socket] = user

            print(f"Connection from {client_address[0]}:{client_address[1]}, user {user['data'].decode()}")

        else:
            message = recv_msg(sock)
            
            if message is False:
                print(f"Closed connection from {clients[sock]['data'].decode()}")
                sockets_list.remove(sock)
                del clients[sock]
                continue
            
            user = clients[sock]
            print(f"Received message from {user['data'].decode()}: {message['data'].decode()}")
            for client in clients:
                client.send(user['header']+user['data']+message['header']+message['data'])

    for sock in exception_sockets:
        sockets_list.remove(sock)
        del clients[sock]