import socket
import sys
from _socket import gethostbyname

print("Wybierz tryb:\n"
      "1. Chce zagrac\n"
      "2. Chce ogladac")
mode = int(input())
if mode == 1:

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if len(sys.argv) != 2 :
        print("Argument format: client.py <IP address> <port> <name>")
        exit()

    server_address = gethostbyname(sys.argv[1])
    print("connecting to:", server_address)
    server.connect((server_address, 80))
    while True:
        move = input("Podaj ruch, jaki chcesz wykonać:")
        server.send(move.encode())
elif mode == 2:
    print("Bedziesz obserwowac.")
else:
    print("Blad, zly wybor!")
