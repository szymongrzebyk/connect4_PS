import socket
import select
import errno
import sys
import struct
from hashlib import sha256
from getpass import getpass
import tlv8

# game imports
from board import *
from control import *
from player import *


class GameEnd(Exception): pass


HEADER_LENGTH = 10
MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

if len(sys.argv) != 4:
    print("Argument format: server.py <IP address> <port>")
    exit()

while True:
    try:
        mode = int(input("1. Play game\n2. Watch game\n"))
        if mode != 1 and mode != 2:
            raise ValueError
        break
    except KeyboardInterrupt:
        sys.exit()
    except:
        print("Choose correct option")

IPaddr = str(sys.argv[1])
port = int(sys.argv[2])
name = str(sys.argv[3])

if mode == 1:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IPaddr, port))

    username = name.encode('utf-8')
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')

    client_socket.send(username_header + username)

    message = client_socket.recv(2048).decode() # initial game message
    print(message)
    if message == "Game full":
        sys.exit()
    while True:
        while True:
            try:
                login = input("Enter your login: ")
                for char in login:
                    if char == ':':
                        raise ValueError
                break
            except ValueError:
                print("\' : \' character is forbidden!")
                continue
        password = getpass("Enter your password:")
        pass_hash = sha256(password.encode('utf-8')).hexdigest()
        TLV_struct = [
            tlv8.Entry(1, login),
            tlv8.Entry(2, pass_hash)
        ]
        creds_data = tlv8.encode(TLV_struct)
        client_socket.send(creds_data)
        reply = ""
        while reply == "":
            reply = client_socket.recv(2048).decode()
        if reply == "WRONG PASS":
            print("Password incorrect.")
        elif reply == 'OK':
            break
        else:
            print("Logging error")
            sys.exit()

else:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    client_socket.bind((MCAST_GRP, MCAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    client_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


def flush_input():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import sys, termios    #for linux/unix
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)


# game preparation
clear_console()
board_width = 7
board_height = 6
board = GameBoard(board_width, board_height)
player1 = Player('O')
player2 = Player('X')
board.print()


# game loop
try:
    if mode==1:
        while True:
            message = ""
            while message == "":
                message = client_socket.recv(2048).decode()
            print(f"Message from server: {message}")
            if message=="Client disconnected":
                raise GameEnd
            if message!="You start":
                try:
                    player2.make_move(board, int(message))
                except GameWon:
                    print("You lost!")
                    raise GameEnd
            flush_input()
            while True:
                message = input("Choose column: ")

                try:
                    player1.make_move(board, int(message))
                    break
                except GameWon:
                    print("You won!")
                    client_socket.send(message.encode())
                    raise GameEnd
                except ValueError:
                        board.print()
                        print("There is no space.")
                except IndexError:
                    board.print()
                    print("No such a column, choose different number.")
            # get input -> validate input -> send input to server
            # -> wait for server response -> print response
            
            # TU DODAĆ WHILE - VALIDATE INPUT
            message = message.encode()
            client_socket.send(message)
    
    else:
        while True:
            message = ""
            while message == "":
                message = client_socket.recv(2048).decode()
            print(f"Message from server: {message}")
            if message=="Client disconnected":
                raise GameEnd
            if message!="You start":
                try:
                    player1.make_move(board, int(message))
                except GameWon:
                    print("Player 1 won!")
                    raise GameEnd
            message = ""
            while message == "":
                message = client_socket.recv(2048).decode()
            print(f"Message from server: {message}")
            if message=="Client disconnected":
                raise GameEnd
            if message!="You start":
                try:
                    player2.make_move(board, int(message))
                except GameWon:
                    print("Player 2 won!")
                    raise GameEnd
            
except GameEnd:
    sys.exit()
    