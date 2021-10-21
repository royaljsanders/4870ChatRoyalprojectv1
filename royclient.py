#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Client
import socket
import time

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
    #try:
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((HOST, SERVER_PORT))
    while True:
        #clientsocket.sendall(b'Test')
        data = clientsocket.recv(MAX_LINE)
        print(data)

        if not data:
            print('.')
            time.sleep(1) #sleep for 1 second
            # TODO recursive check if not data, lost cennection to the server?
            # print something like "Trying to reconnect... in %d (sec)"
            pass
        else:
            print(data)
            answer = input()
            if answer == 'q!':
                break

            clientsocket.sendall(answer.encode())
    print("Closing socket...")
    clientsocket.close()
    print("Socket closed.")
    return 0
'''
        except:
            print('something went wrong')
            # TODO: better error handling
'''


if __name__ == "__main__":
    main()
