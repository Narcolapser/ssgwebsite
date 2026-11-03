# Like the client this is the only library we need for networking.
import socket

# However, since we are also running commands, we'll need this as well
import subprocess

# First we need a socket, this base most piece of software is what we will
# build everything on. It is instantiated with two constants:
# AF_INET: Address Family INet. I couldn't find any definative evidence on
#   what "INET" stands for so I think of it as "InterNET" as it refers
#   specifically to IPv4. You could also do AF_INET6 if you needed to
#   communicate over IPv6
# SOCK_STREAM: One of a couple of options, though the only other one that
#   appears to be useful these days is "SOCK_DGRAM" or Datagram protocol.
#   While it doesn't explicitly say it in the documentation, it appears that
#   SOCK_DGRAM is used to get a UDP socket. SOCK_STREAM however is  used to
#   get a TCP socket.
# Most of the time these are the two you will want, it is all I've ever used.
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Here we are setting the socket to be reusable. This allows us to start and
# stop the server without having to wait for the socket to close.
# SOL_SOCKET: I hate to say "Just put it in." But that's about all I could find.
#   The documentation around this option just says: 
#       Level number for (get/set)sockopt() to apply to socket itself.
#   With no indication of what other options there might be. So put SOL_SOCKET
#   into this command to effect socket level values.
# SO_REUSEADDR: Socket Option Reuse Address. Allow local address reuse
# 1: Set this option to true.
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# We next bind to the address in question. 0.0.0.0 means any address. Here we
# are using 10023 instead of just 23 as you need special permissions to use the
# ports 1-1024 on most machines. Again, passed in as a tuple. It is done this
# way because (ip, port) together create one address. For different address
# families it may be formatted differently. For AF_INET it's a tuple with ip and
# port number. 
sock.bind(('0.0.0.0',10023))

# Tell the socket to listen for incoming connections. We will only be waiting
# for a single connection since we are keeping this simple.
sock.listen(1)

# Get hostname for display later.
hostname = socket.gethostname()

# Message to send on connection. Not that sockets want byte strings.
motd = b'You have connected to a example server. \r\n'

# Because we aren't doing an exercise in threading we will be doing some unsafe
# practices later on. This warning foreshadows that.
motd += b'Only run commands that self terminate. \r\n' + hostname.encode() + b'> '

# Loop forever.
while True:
    try:
        # First we wait for a connection
        con, addr = sock.accept()
        print(addr)
        
        # Send the Message of the day
        con.send(motd)
        
        # Monitor variable
        active = True
        
        # Loop until the connection is closed
        while active:
            # When receiving user commands terminate with a new line, \r\n. So 
            # we will loop until that new line has been received.
            command = con.recv(1)
            while command[-1] != 10:
                command += con.recv(1)
            
            # Check if the user intends to close the connection:
            if command == b'quit\r\n':
                active = False
                continue
            
            # Next we call the command. Some quick notes to the uninitiated on
            # the use of this particular command. Subprocess spawns a new child
            # process thread by calling, as if in the terminal, the command that
            # is passed in. This command must be in the form of a list. This is
            # part of the sanitation process and keeps you from accidentally 
            # blowing your machine up. So we take the command string from above
            # and use split to seperate it out into a list of strings.
            # Also, as I foreshadowed above, this is not an asynchronus task. It
            # will not return until the command that is called returns. Which
            # means something like 'ping' would effectly crash the server.
            outs = subprocess.check_output(command.split())
            
            # Return the result
            con.send(outs)
            
            # And some nice formating.
            con.send(hostname.encode() + b'> ')

        con.close()
    except Exception as e:
        print('Connection had a oopsie: ', type(e), e)
