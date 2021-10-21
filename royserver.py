#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Server
import socket
import traceback

__HOST =       '127.0.0.1' #loopback
__SERVER_PORT = 11138
__MAX_PENDING = 5
MAX_LINE    = 256

# Written by Royal
# adapted from skeleton.c and online:
# https://docs.python.org/3/howto/sockets.html
# https://realpython.com/python-sockets/
# https://docs.python.org/3/library/socket.html#socket-objects
# https://stackoverflow.com/a/50997965

# 1create a socket
# 2bind the socket
# 3listen on the socket
# 4while 1 accept connections {
    # 5send and receive data
# } 6close socket (which is handled by the with statement) TODO: do it the hard way?

def main():

    # TODO: Bring in users file.


    f = open("users.txt","r")
    lines = f.readlines()
    print("lines")
    for line in lines:
        print(line)
    # TODO: better error handling


    # 1create a socket
    print("Server is starting and creating a socket...", end=' ')
    # create an INET, STREAMing socket
    # serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Garbage collection would take care of a socket, and so does with, but
    # I'll explicitly close it to make sure I get full points
    # TODO: move this while loop down as far as possible, so it goes between the correct step
    #accept connections {

    try:


        print("Server is starting and creating a socket...", end=' ')
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 2bind the socket
        # bind the socket to a host, and a port
        print("Done.\nBinding...")
        serversocket.bind((__HOST, __SERVER_PORT))


        while(True):
            try:
                # 3listen on the socket
                print("Listening and accepting connections...")
                serversocket.listen(__MAX_PENDING)

                # 4 Accept connectionspy
                print("Waiting for client to connect...")
                conn, addr = serversocket.accept()

                with conn:
                    while(True):
                        # Loop before logging in (Authentication Loop)
                        print('Connected by', addr)
                        #data = conn.recv(MAX_LINE)

                        intro = b'Hello Client! Welcome to the Echo Chamber.\nDo you want to create a New User (N/n), or Log in (L/l)?: '
                        #send 'intro for client' from server
                        conn.sendall(intro)
                        data = conn.recv(MAX_LINE)
                        if not data:
                            pass
                        else:
                            print(addr, ":", data)



                    # The loop after logging in (Messaging Loop)
                    while True:
                        data = conn.recv(MAX_LINE)

                        if not data:
                            pass
                        else:
                            print("Messaging: data", data)

                            # 5send and receive data
                            # TODO: Login, NewUser.
                                # Verify Login
                            # TODO: Send, Logout?
                            #send 'intro for client' from server
                            intro = b'Hello Client! Welcome to the Echo Chamber.\nDo you want to create a New User (N/n), or Log in (L/l)?: '
                            #send 'intro for client' from server
                            conn.sendall(intro)



                            #get 'login or new user' options from client
                            clientmsg = conn.recv(MAX_LINE)

                            # TODO: checking to make sure this var is safe
                            if not clientmsg: break
                            if clientmsg == 'q!': break
                            print(clientmsg)


                        #confirmation message

                        #send

                        #new user
            except BrokenPipeError:
                print("Lost connection with :", addr)
        # shutdown() recommended to close "in a timely fashion"
        # https://docs.python.org/3/library/socket.html#socket.socket.shutdown
        print("Closing socket...")
        serversocket.close()
        print("Socket closed.")
        # } 6close socket TODO 30 pts

    except Exception as e:
        #''' #woah you can comment out block comments? trippy
        print("RoyCode has detected a problem and must shut down.")

        print("Closing socket...")
        serversocket.close()
        print("Socket closed.")
        print(e)
        traceback.print_exc()
    #'''
    #except:
        #print('something went wrong')
        # TODO: better error handling for message input. Perhaps a function like isascii? does that exist?
    return 0

if __name__ == "__main__":
    main()
