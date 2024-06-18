import socket
import select
import errno
import sys

HEADER_LENGTH = 10

if len(sys.argv) != 4:
    print("Argument format: server.py <IP address> <port>")
    exit()

IPaddr = str(sys.argv[1])
port = int(sys.argv[2])
name = str(sys.argv[3])

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IPaddr, port))

username = name.encode()
username_header = f"{len(username):<{HEADER_LENGTH}}".encode()
client_socket.send(username_header + username)

while True:
    message = input("Choose column: ")

    # get input -> validate input -> send input to server
    # -> wait for server response -> print response
    if message:
        message = message.encode()
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode()
        client_socket.send(message_header + message)

    try:
        while True:
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print("Connection closed by server")
                sys.exit()
            username_length = int(username_header.decode().strip())
            username = client_socket.recv(username_length).decode()

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode().strip())
            message = client_socket.recv(message_length).decode()

            print(f"{username} > {message}")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error',str(e))
            sys.exit()
        continue

    except Exception as e:
        print('General error',str(e))
        sys.exit()