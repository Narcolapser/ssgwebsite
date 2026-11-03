import socket
import sys

# Our client will be called with 2 arguments, the server to connect to and the nickname we wish to use.
if len(sys.argv) < 3:
    print("Called with 2 arguments: Server nick (optional: port)")
    sys.exit(1)

# Extract the server
server = sys.argv[1]
# Extrac the nick name
nick = sys.argv[2]
# If the server is on an unusual port, extract that to, other wise 6667
if len(sys.argv) > 3:
    port = int(sys.argv[3])
else:
    port = 6667

# Instantiate the socket
con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to the server.
con.connect((server, port))
# Set a time out.
con.settimeout(1)

# send the initial commands, first who I am.
con.send('NICK {}\r\n'.format(nick).encode('utf-8'))
# Second, where I am connecting from.
con.send('USER {0} {0} {1} :{0}\r\n'.format(nick, '192.236.35.165').encode('utf-8'))

# A quit flag to track when the user wants to close the client.
quit = False
# A way to track which channel we are in. For simplicity sake we are only going to work with one channel.
channel = None

# Loop until the user wants to quit.
while not quit:
    # A prompt with an arrow as such indicates to most users that we are waiting for input.
    ins = input("> ")

    # If the user passes a blank line we check the server. This was a compromise that was made to keep this simple. It
    # turns out requesting input from the command line asynchronously is not straight forward. So rather than have a
    # long complicated piece of code to do such, we just let the user press enter to check for new chats.
    if ins == '' or ins == 'refresh':
        try:
            # Print new messages
            print(con.recv(1024).decode('utf-8'))
        except socket.timeout:
            pass
        continue

    # If the input starts with a forward slash, it is a command.
    if ins[0] == '/':
        # split the command into the command and arguments.
        command = ins[1:].split(' ')
        if len(command) > 1:
            args = command[1:]
        else:
            args = []

        # To avoid case sensitivity, all to lower.
        command = command[0].lower()

        # Join command joins you to a channel.
        if command == 'join':
            if len(args) == 0:
                # If the user fails to specify a channel, print out a tip
                print('/Join needs a channel')
                continue
            if args[0][0] != '#':
                # Channels start with "#" so if the user sends a channel without one, inform them.
                print('Channels must start with a hash "#"')
                continue

            # If the command checks out, join that channel locally and request the same fromt he server.
            channel = args[0]
            con.send('join {}'.format(channel).encode('utf-8') + b'\r\n')

        # Leave a channel.
        elif command == 'part':
            con.send(b'PART ' + ' '.join(args).encode('utf-8'))

        # Quit the server and close the program.
        elif command == 'quit':
            quit = True
            con.send(b'QUIT :leaving\r\n')
        # Any further commands that you wish to implement would go here, before the default case.

        else:
            print('command not recognized')

    # If the user's input isn't a command, it must be a message.
    else:
        # Check that the user is in a channel. You can't chat unless you are chatting somewhere.
        if not channel:
            print('you must /join a channel first')
            continue

        # Send the message to the channel we are currently in.
        con.send('privmsg {} :{}'.format(channel, ins).encode('utf-8') + b'\r\n')

    try:
        # Check if there is anything to print.
        print(con.recv(1024).decode('utf-8'))
    except socket.timeout:
        pass

# Gracefully close the connection to the remote server.
con.close()