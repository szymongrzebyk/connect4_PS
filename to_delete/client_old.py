import socket
import sys
import select
from _thread import *

print("Wybierz tryb:\n"
      "1. Chce zagrac\n"
      "2. Chce ogladac")
mode = int(input())
if mode == 1:

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if len(sys.argv) != 4 :
        print("Argument format: client.py <IP address> <port> <name>")
        exit()

    # server_address = socket.gethostbyname(sys.argv[1]) # to add later: DNS
    IPaddr = str(sys.argv[1])
    port = int(sys.argv[2])
    print("connecting to:", str(sys.argv[1]))
    server.connect((IPaddr, port))
    name = str(sys.argv[3])

    # while True:
    #     socket_list = [socket.socket(), server]
    #     read_sockets, write_socket, error_socket = select.select(socket_list, [], [])
        
    #     for sock in read_sockets:
    #         if sock==server:
    #             recv_msg = sock.recv(2048)
    #             if not recv_msg:
    #                 sys.exit(0)
    #             message = recv_msg.decode()
    #             print(message)
    #         else:
    #             print("Podaj ruch, jaki chcesz wykonać: ", end='')
    #             move = sys.stdin.readline()
    #             server.send(move.encode())
    #             sys.stdout.write(f"You chose column ")
    #             sys.stdout.write(move)
    #             sys.stdout.flush()


    server.close()

elif mode == 2:
    print("Bedziesz obserwowac.")
    # to add: multicast receive
else:
    print("Blad, zly wybor!")