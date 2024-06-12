import socket
import sys
from _thread import start_new_thread

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) > 1:
    print("Argument format: server.py <IP address> <port>")
    exit()

ip_address = "192.168.1.38"
server.bind((ip_address, 80))
print("Binded")
server.listen(2)
print("listening")

clients = []


def clientthread(conn, addr):
    # conn.send("Welcome to the chatroom".encode())
    while True:
        try:
            message = (conn.recv(2048)).decode()
            if message:
                message_to_send = f"[{addr[0]}] {message}"
                print(message_to_send)
                broadcast(message_to_send, conn)
            else:
                rm_conn(conn)
        except:
            continue


def broadcast(message,conn):
    for client in clients:
        if client!=conn:
            try:
                client.send(message.encode())
            except:
                client.close()
                rm_conn(client)


def rm_conn(conn):
    if conn in clients:
        clients.remove(conn)


while True:
    conn, addr = server.accept()
    clients.append(conn)

    print(f"{addr[0]} connected")
    start_new_thread(clientthread, (conn, addr))


conn.close()
server.close()
