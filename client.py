import socket
import select
import errno
import sys
import pickle

HEADER_LENGTH = 10

if len(sys.argv) != 4:
    print("Argument format: server.py <IP address> <port>")
    exit()

IPaddr = str(sys.argv[1])
port = int(sys.argv[2])
name = str(sys.argv[3])

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IPaddr, port))
# client_socket.setblocking(False)

username = name.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')

client_socket.send(username_header + username)

message = client_socket.recv(2048).decode() # initial game message
print(message)
if message == "Game full":
    sys.exit()


while True:
    message = ""
    while message == "":
        message = client_socket.recv(2048).decode()
    print(f"Message from server: {message}")

    message = input("Choose column: ")

    # get input -> validate input -> send input to server
    # -> wait for server response -> print response
    
    # TU DODAĆ WHILE - VALIDATE INPUT
    message = message.encode()
    message_header = f"{len(message):<{HEADER_LENGTH}}".encode()
    client_socket.send(message_header + message)

    