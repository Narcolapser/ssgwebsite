# The only library we'll be needing.
import socket

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
con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# We will be connecting to an open telnet server with a few utilities on it.
# Replace this line with whatever server you might be interested in
# connecting to along with the appropriate port, usually 23.
con.connect(('telehack.com', 23))

# We are going to use a time out to provide interactive behavior. In a more
# serious setting this would not be acceptable. But as this is an exercise
# in telnet not in threading we are going to use the easy way.
con.settimeout(1)


def handle_command(con):
    # Recieve the command byte
    command = con.recv(1)
    item = con.recv(1)

    # Check the byte against the known options.
    # These handles are left as place holders. Should there be desire to develop
    # this simple script into a more real client these handlers would need to be
    # more fleshed out. But the idea of how commands in general would be handled
    # is demonstrated here. Specifics are left as an exercise to the reader.
    if command == b'\xfe':  # 254
        print('dont: {}'.format(int(item.hex(), 16)))
    elif command == b'\xfd':  # 253
        print('do: {}'.format(int(item.hex(), 16)))
    elif command == b'\xfc':  # 252
        print('wont: {}'.format(int(item.hex(), 16)))
    elif command == b'\xfb':  # 251
        print('will: {}'.format(int(item.hex(), 16)))
    else:
        # If the command is unknown print it to screen. There are more than
        # these four but I've left them off for brevity. 
        print('Unknown command: {}'.format(command))


# Variable to track when the loop is done.
eof = False

# Loop until the connection is closed at either end.
while not eof:

    # Loop as long as there is a byte to receive within one second.
    receiving = True
    while receiving:
        try:
            # This is not effecient, but it is simple. We receive a byte and
            # then process it. It would be more effecient to recieve as much
            # as is in the buffer and then process it so the code isn't going
            # back and forth to IO, but this makes the concept easy to
            # understand. 
            val = con.recv(1)

            # Check if the byte is the signal for a command.
            if val == b'\xff':  # Interpret as command
                handle_command(con)
            # Other wise we just print it
            else:
                print(val.decode('ascii'), end='')

        except socket.timeout:
            # No byte recieved for 1 second. They probably won't send any more
            # until we interact. Step out of the receiving loop and ask for
            # user input now.
            receiving = False

        except ConnectionResetError:
            # Our connection was lost, Close the program.
            eof = True

    # Request input from user.
    response = input('> ')

    # If the command is 'quit' the user intends to close the connection.
    if response == 'quit':
        eof = True

    try:
        # Send the input to the server with a line brake.
        con.send(response.encode() + b'\r\n')
    except ConnectionResetError:
        # Connection was closed, Close the program.
        eof = True

# Cleaning up: Close your socket!        
con.close()

# Inform the user the connection has closed.
print('Connection closed')
