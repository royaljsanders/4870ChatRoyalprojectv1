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

#def newuser(user, pasw):
    #try:
        #clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #clientsocket.connect((HOST, SERVER_PORT))

        #command = "^NU_" + user + "^PW_" + pasw
        #clientsocket.sendall(bytes(command, 'utf-8'))
        #print("Request sent, waiting")
        #reply = clientsocket.recv(MAX_LINE)
        #print(reply.decode())

        #same sending message loop as login, our socket is in local function scope so let's keep using it.
        #while(True):
            #if not reply:
                #clientsocket.close()
                #return False

            #selectstr = input()
            #select = selectstr.split()
            #print(type(select), select)
            #if New User
            #if (select[0] == 'newuser'):
                #print("Denied. Logout first to create a new user.")
            #logging in
            #elif (select[0] == 'login'):
                #print("Denied. Already logged in.")

            #elif (select[0] == 'send'):
                #select = selectstr.split(maxsplit=1)
                #print(type(select[1]), select[1])
                #clientsocket.sendall(select[1].encode())

                #reply = clientsocket.recv(MAX_LINE)
                #print(reply.decode())
                #continue

            #elif (select[0] == 'logout'):
                #print("Closing socket...")
                #clientsocket.close()
                #print("Socket closed.")
                #return False

            #else:
                #print("Unrecognized command.")
                #continue

        #print("Closing socket...")
        #clientsocket.close()
        #print("Socket closed.")
    #except KeyboardInterrupt:
        #print("KeyboardInterrupt detected. Leaving chatroom.")
        #print("Closing socket...")
        #clientsocket.close()
        #print("Socket closed.")
    #except ConnectionRefusedError:
        #print("Server is not available right now.")
        #clientsocket.close()
    #except Exception as e:
        #print("New error! Nice. \nRoyClient has detected a problem with creating New user.")
        #clientsocket.close()
        #print(e)
        #traceback.print_exc()

    #return False # if can connect

def login(user, pasw, newuser=False):
    try:
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect((HOST, SERVER_PORT))
        if (newuser == True):
            command = "^NU_" + user + "^PW_" + pasw
        else:
            command = "^LI_" + user + "^PW_" + pasw
        clientsocket.sendall(bytes(command, 'utf-8'))
        #print("User Logged in, waiting...")
        reply = clientsocket.recv(MAX_LINE)
        print(reply.decode())
        if (newuser == True):
            time.sleep(1)
            print("returning to main")
            return False

        # This is the loop of sending messages
        while(True):
            if not reply:
                clientsocket.close()
                return False


            selectstr = input()
            select = selectstr.split()
            #print(type(select), select)
            # if New User
            if (select[0] == 'newuser'):
                print("Denied. Logout first to create a new user.")
                # logging in

            elif (select[0] == 'login' and newuser == False):
                print("Denied. Already logged in.")
            elif (select[0] == 'login' and newuser == True):
                print("Denied. Already new userd in.")

            elif (select[0] == 'send'):
                select = selectstr.split(maxsplit=1)
                #print(type(select[1]), select[1])
                clientsocket.sendall(select[1].encode())

                reply = clientsocket.recv(MAX_LINE)
                print(reply.decode())
                continue

            elif (select[0] == 'logout'):
                #print("Closing socket...")
                clientsocket.close()
                #print("Socket closed.")
                return False

            else:
                print("Unrecognized command.")
                continue


        #print("Closing socket...")
        clientsocket.close()
        #print("Socket closed.")
    except KeyboardInterrupt:
        print("KeyboardInterrupt detected. Shutting down.")
        print("Closing socket...")
        clientsocket.close()
        print("Socket closed.")
    except ConnectionRefusedError:
        print("Server is not available right now.")
    except IndexError:
        print("Denied. Incorrect command usage.")
    except Exception as e:
        print("New error! Nice. \nRoyClient has detected a problem with Logging in")
        print(e)
        traceback.print_exc()

    return False # if cannot connect

def main():
    print("My chat room client. Version One.\n")
    while(True):
        try:
            selectstr = input()
            select = selectstr.split()
            #print(type(select), select)
            # if New User
            if (select[0] == 'newuser'):
                user = select[1]
                pasw = select[2]
                # The length of the UserID should be between 3 and 32 characters,
                if (len(user) < 3 or len(user) > 32):
                    print("Denied. The Username must be between 3 and 32 characters.")
                    continue

                # The length of the UserID should be between 3 and 32 characters,
                if (len(pasw) < 4 or len(pasw) > 8):
                    print("Denied. The Username must be between 3 and 32 characters.")
                    continue
                if (login(user, pasw, newuser=True) == False):
                    continue

            # logging in
            elif (select[0] == 'login'):
                user = select[1]
                # The length of the UserID should be between 3 and 32 characters,
                pasw = select[2]

                if (login(user, pasw) == False):
                    # logout invoked
                    return


            elif (select[0] == 'send'):
                print("Denied. Please login first.")
                continue

            elif (select[0] == 'logout'):
                # just straight up closing.
                return

            else:
                print("Unrecognized command.")
                continue
        except IndexError:
            print("Denied. Incorrect command usage.")
        except ConnectionRefusedError:
            print("Server is not available right now.")
            continue
        except Exception as e:
            print("RoyClient has detected a problem and must shut down.")

            print(e)
            traceback.print_exc()


if __name__ == "__main__":
    main()
