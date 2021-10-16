#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Client
import socket

HOST =       '127.0.0.1' #loopback
SERVER_PORT = 11138
MAX_LINE    = 256


# Written by Royal
# Client

# translate the server name or IP address (128.90.54.1) to resolved IP address
# If the user input is an alpha name for the host, use gethostbyname()
# If not, get host by addr (assume IPv4)
# Create a socket.
# Connect to a server.
# Send and receive data.
# closesocket(s); TODO: do it the hard way?

def main():
    print("Client is starting")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientsocket:
    #try:
        clientsocket.connect((HOST, SERVER_PORT))
        clientsocket.sendall(b'Hello World! --from Client.')
        data = clientsocket.recv(1024) #TODO: maxline?
        print("data", data)
    return 0
'''
        except:
            print('something went wrong')
            # TODO: better error handling
'''


if __name__ == "__main__":
    main()
