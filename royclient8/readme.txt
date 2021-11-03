Current python version on my machine is 3.9.7.
I've also tested it at work which I think is on 3.7 or something older than 3.9.7

I expect any version of Python 3.x.x would work, but I can't say for certain.
All you need to do to run the programs will be the normal way of running python programs:

First, navigate to the directory containing these files. You will need to have two terminals open.
    To start the server:    python royserver.py
    To start the client:    python royclient.py
    To stop the server:     KeyboardInterrupt (typically Ctrl+C)
    # Stopping the server uses a KeyboardInterrupt since it needs to listen, and no multithreading (yet).

You should be able to start them in either order, but of course if the server is not running the client can't do much.
