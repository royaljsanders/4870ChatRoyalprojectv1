#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Client
import socket
import traceback
import time


HOST =       '127.0.0.1' #loopback
SERVER_PORT = 11138
MAX_LINE    = 256

# TODO: ConnectionRefusedError



# Written by Royal
# Client Royal Sanders, 11/1, This is the client program that implements basic socket API usage.

# translate the server name or IP address (128.90.54.1) to resolved IP address
# If the user input is an alpha name for the host, use gethostbyname()
# If not, get host by addr (assume IPv4)
# ^ wonder where these 3 comments came from?
# Create a socket.
# Connect to a server.
# Send and receive data.

# ^NU_ new user
# ^LI_ log in
# ^LO_ log out
# ^MS_ message
def newuser(user, pasw):
    try:
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect((HOST, SERVER_PORT))
        #
        command = "^NU_" + user + "^PW_" + pasw
        clientsocket.sendall(bytes(command, 'utf-8'))
        print("Request sent, waiting")
        reply = clientsocket.recv(MAX_LINE)
        print(reply.decode())

        # same sending message loop as login, our socket is in local function scope so let's keep using it.
        while(True):
            if not reply:
                clientsocket.close()
                return False

            # probably prepend with the command: login, newuser, message, logout
            message = input("Send: ")
            clientsocket.sendall(message.encode())

            reply = clientsocket.recv(MAX_LINE)
            print(reply.decode())

        print("Closing socket...")
        clientsocket.close()
        print("Socket closed.")
    except KeyboardInterrupt:
        print("KeyboardInterrupt detected. Leaving chatroom.")
        print("Closing socket...")
        clientsocket.close()
        print("Socket closed.")
    except ConnectionRefusedError:
        print("Server is not available right now.")
        clientsocket.close()
    except Exception as e:
        print("New error! Nice. \nRoyClient has detected a problem with creating New user.")
        clientsocket.close()
        print(e)
        traceback.print_exc()

    return False # if can connect

def login(user, pasw):
    try:
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect((HOST, SERVER_PORT))
        #
        command = "^LI_" + user + "^PW_" + pasw
        clientsocket.sendall(bytes(command, 'utf-8'))
        print("User Logged in, waiting...")
        reply = clientsocket.recv(MAX_LINE)
        print(reply.decode())

        # This is the loop of sending messages
        while(True):
            if not reply:
                clientsocket.close()
                return False

            # probably prepend with the command: login, newuser, message, logout
            message = input("Send: ")
            clientsocket.sendall(message.encode())

            reply = clientsocket.recv(MAX_LINE)
            print(reply.decode())

        print("Closing socket...")
        clientsocket.close()
        print("Socket closed.")
    except KeyboardInterrupt:
        print("KeyboardInterrupt detected. Shutting down.")
        print("Closing socket...")
        clientsocket.close()
        print("Socket closed.")
    except ConnectionRefusedError:
        print("Server is not available right now.")
    except Exception as e:
        print("New error! Nice. \nRoyClient has detected a problem with Logging in")
        print(e)
        traceback.print_exc()

    return False # if can connect

def main():
    print("Client is starting")
    while(True):
        try:
            select = input("Do you want to create a New User (N/n), Log in (L/l), or Quit (Q/q)?: ")
            # if New User
            if (select == 'N') or (select == 'n'):
                user = input("Please enter a username between 3 and 32 characters: ")
                # The length of the UserID should be between 3 and 32 characters,
                if (len(user) < 3 or len(user) > 32):
                    print("The Username must be between 3 and 32 characters.")
                    continue
                pasw = input("Please enter a password between 4 and 8 characters: ")
                # The length of the UserID should be between 3 and 32 characters,
                if (len(pasw) < 4 or len(pasw) > 8):
                    print("The Username must be between 3 and 32 characters.")
                    continue
                if (newuser(user, pasw)):
                    print("Invoked ^NU_")

            # logging in
            elif (select == 'L') or (select == 'l'):
                user = input("Username: ")
                # The length of the UserID should be between 3 and 32 characters,
                pasw = input("Password: ")

                if (login(user, pasw)):
                    # can only call the message function if logged in.
                    print("login returned true")
                    break
                else:
                    print("Not logged in. This might mean you told the server you wanted to quit.\n You can try logging in again if you like." )
                    continue
                # send to server and check, see if log in.
                # if logged in, call the logged in function. (to prevent automatic anon logins)
                # if not able to log in, try the loop again

            elif (select == 'Q') or (select == 'q'):
                # quit
                return

            else:
                print("Unrecognized command. Try again, or use (Q/q) to quit.")
                continue

        except ConnectionRefusedError:
            print("Server is not available right now.")
            continue
        except Exception as e:
            print("RoyClient has detected a problem and must shut down.")

            print(e)
            traceback.print_exc()


if __name__ == "__main__":
    main()
