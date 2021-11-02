"""
Written by Royal
adapted from skeleton.c and online:
https://docs.python.org/3/howto/sockets.html
https://realpython.com/python-sockets/
https://docs.python.org/3/library/socket.html#socket-objects
https://stackoverflow.com/a/50997965

Royal Sanders, 11/1, This is the server program that implements basic socket API usage.
Right now, the server allows 1 connection at a time.
"""
import socket
import traceback
import string

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

# ^NU_ new user
# ^LI_ log in
# ^LO_ log out
# ^MS_ message

# returns True if login data corresponds to a user in our file.
def newuser(messagestr):

    # just need to add to file. We assume clients haven't hacked anything
    print("Need to add this user, then log in.")
    authstr = messagestr.replace(bytes("^NU_", 'utf-8'), bytes('^LI_', 'utf-8'))
    if (authenticate(authstr) != False):
        #tell user that wasn't right
        pass
    else:
        try:
            messagestr = messagestr.replace(bytes("^NU_", 'utf-8'), bytes('', 'utf-8'))
            print(messagestr)
            userbytes, trash, passbytes = messagestr.partition(bytes("^PW_", 'utf-8'))
            externaluser = userbytes.decode()
            externalpasw = passbytes.decode()

            f = open("users.txt","a")
            addstr = "(" + externaluser + ", " + externalpasw + ")"
            print("addstr", addstr)
            f.write('\n'+addstr)
            f.close()
            return authenticate(authstr)
        except Exception as e:
            print("New error! Nice. \nRoyClient has detected a problem with creating New user.")
            print(e)
            traceback.print_exc()
    return False

def authenticate(messagestr):
    try:
        print("messagestr from auth)", messagestr)
        f = open("users.txt","r")
        filelines = f.readlines()
        #print("Users")

        userlist = []

        # cleaning file stuffs into just what I need: username and passwords as strings.
        for line in filelines:
            line = line.replace(' ', '')
            line = line.replace('\n', '')
            line = line.replace('(', '')
            line = line.replace(')', '')
            linelist = line.split(',')
            for strang in linelist:
                pass

            userlist.append(linelist)

        #for line in userlist:
            #print("_%s.%s_" % (line[0], line[1]))

        messagestr = messagestr.replace(bytes("^LI_", 'utf-8'), bytes('', 'utf-8'))
        print(messagestr)
        userbytes, trash, passbytes = messagestr.partition(bytes("^PW_", 'utf-8'))
        # partition the byte string and then convert the parts we want to keep to utf-8
        externaluser = userbytes.decode()
        externalpasw = passbytes.decode()

        for row in userlist:
            if (externaluser == row[0] and externalpasw == row[1]):
                print("User %s signed in" % externaluser)
                return externaluser
            else:
                continue
    except IndexError as i:
        print(i)
        print("There is likely a problem with the users.txt file.")
        traceback.print_exc()
    except Exception as e:
        print("New error! Nice. \nRoyClient has detected a problem with Logging in user.")
        print(e)
        traceback.print_exc()

    return False

def main():
    # serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Garbage collection would take care of a socket, and so does with, but


    try:
        # 1 create an INET, STREAMing socket
        print("Server is starting and creating a socket...", end=' ')
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Very bottom of this page tells us how to deal with socket wait time if an error occurs
        # https://docs.python.org/3/library/socket.html
        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # 2bind the socket
        # bind the socket to a host, and a port
        print("Done.\nBinding...")
        serversocket.bind((__HOST, __SERVER_PORT))

                        # 3listen on the socket
        print("Listening and accepting connections...")
        serversocket.listen(__MAX_PENDING)


        while(True):
            try:
                # 4 Make new connection.
                print("Waiting for client to connect...")
                conn, addr = serversocket.accept() # conn is a NEW SOCKET

                # Very bottom of this page tells us how to deal with socket wait time if an error occurs
                # https://docs.python.org/3/library/socket.html
                #conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                # also trying outside of loop

                with conn:
                    # Loop before logging in (Authentication Loop)
                    print('Connected by', addr, end='')
                    #data = conn.recv(MAX_LINE)

                    #intro = b'Hello Client! Welcome to the Echo Chamber.\n'
                    #send 'intro for client' from server
                    #conn.sendall(intro)
                    data = conn.recv(MAX_LINE)
                    if not data:
                        pass
                    else:
                        # handle log in / new user commands.
                        print(type(data), '\n', data)
                        if (data.startswith(bytes("^LI_", 'utf-8'))):
                            username = authenticate(data)
                            if(username != False):
                                print('External User Authenticated. Letting them into the chat room...')
                                # TODO if authenticate passes, then we can send over to messaging area.
                                # when the user logs out, it will control flow brings us back here to disconnet.
                                intro = b"Hello Client! Welcome to the Echo Chamber.\nSend your message, or '!q' to quit."
                                #send 'intro for client' from server
                                conn.sendall(intro)
                                print("User Logged in, waiting on messages now.")
                                while(True):
                                    clientmsg = conn.recv(MAX_LINE)
                                    if not clientmsg:
                                        print("Lost connection with a client. Accepting new client...")
                                        break

                                    else:
                                        if clientmsg.decode() == '!q':
                                            break
                                        echomsg = username + ": " + clientmsg.decode()
                                        print(echomsg)
                                        conn.sendall(bytes(echomsg, 'utf-8'))

                            else:
                                print('External User Incorrect Info. Tell them to try again.')
                                # TODO reject the connection politely

                        elif (data.startswith(bytes("^NU_", 'utf-8'))):
                            username = newuser(data)
                            if(username != False):
                                print('New User Authenticated. Letting them into the chat room...')
                                intro = b"Hello Client! Welcome to the Echo Chamber. \nSend your message, or '!q' to quit."
                                #send 'intro for client' from server
                                conn.sendall(intro)
                                print("User Logged in, waiting on messages now.")
                                while(True):
                                    clientmsg = conn.recv(MAX_LINE)
                                    if not clientmsg:
                                        print("Lost connection with a client. Accepting new client...")
                                        break

                                    else:
                                        if clientmsg.decode() == '!q':
                                            break
                                        echomsg = username + ": " + clientmsg.decode()
                                        print(echomsg)
                                        conn.sendall(bytes(echomsg, 'utf-8'))

                            else:
                                print('External User Incorrect Info. Tell them to try again.')
                                # TODO reject the connection politely
                        else:
                            # TODO don't accept or try again
                            break #?

            except BrokenPipeError:
                print("Lost connection with :", addr)
        # shutdown() recommended to close "in a timely fashion"
        # https://docs.python.org/3/library/socket.html#socket.socket.shutdown
        print("Closing socket...")
        serversocket.close()
        print("Socket closed.")
        # I'll explicitly close it to make sure I get full 30 points here.

    except KeyboardInterrupt:
        print("KeyboardInterrupt detected. Shutting down.")
        print("Closing socket...")
        serversocket.close()
        print("Socket closed.")
    except Exception as e:
        #''' #woah you can comment out block comments? trippy
        print("RoyServer has detected a problem and must shut down.")

        print("Closing socket...")
        serversocket.close()
        print("Socket closed.")
        print(e)
        traceback.print_exc()
    return 0

if __name__ == "__main__":
    main()
