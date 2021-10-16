#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Server
import socket

__HOST =       '127.0.0.1' #loopback
__SERVER_PORT = 11138
__MAX_PENDING = 5
__MAX_LINE    = 256

# Written by Royal
# adapted from skeleton.c and online:
# https://docs.python.org/3/howto/sockets.html
# https://realpython.com/python-sockets/

# 1create a socket
# 2bind the socket
# 3listen on the socket
# 4while 1 accept connections {
    # 5send and receive data
# } 6close socket

def main():
    print("Server is starting and creating a socket...", end=' ')

    # TODO: better error handling

    # 1create a socket
    # create an INET, STREAMing socket
    # serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
        try:
            # 2bind the socket
            # bind the socket to a host, and a port
            print("Done.\nBinding...")
            serversocket.bind((__HOST, __SERVER_PORT))

            # 3listen on the socket
            print("Listening and accepting connections...")
            serversocket.listen()

            # 4 Accept connections
            conn, addr = serversocket.accept()
            print("Accepted a connection!")

            # while 1 accept connections {
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    # 5send and receive data
                    conn.sendall(data)


            # } 6close socket

            pass
        except:
            print('something went wrong')
            # TODO: better error handling
    return 0

if __name__ == "__main__":
    main()
