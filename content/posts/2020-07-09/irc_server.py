import socket

# Request a TCP Socket.
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Allow us to re-use the same port quickly.
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind to any traffic coming in on port 6667.
sock.bind(('0.0.0.0', 6667))

# Unlike other applications I have made in this series, we have to be able to manage multiple clients at once. This
# means we have to be a little more creative. We'll timeout on the socket accept so if no one is trying to connect, we
# will just continue.
sock.settimeout(1)

# Finally listen to that port for an incoming connection.
sock.listen(2)

# The list of connections
users = []

# Loop forever.
while True:
    # I have put it all inside of a try block here so that you can gracefully shut down the server on keyboard escape.
    try:

        try:
            # See if anyone is waiting.
            con, addr = sock.accept()
            user, nick = None, None

            while not user or not nick:
                # Get their opening request, this will most likly include both user and nick commands.
                message = con.recv(1024).decode('utf-8')
                # Split the message into commands:
                commands = message.split('\r\n')
                for command in commands:
                    args = command.split(' ')
                    if args[0] == 'NICK':
                        nick = command[5:]
                    elif args[0] == 'USER':
                        user = args[1]
            # Add the user object to the list of users.
            users.append({'con':con, 'user': user, 'nick': nick, 'channels':[]})

            # Set a time out on the connection.
            con.settimeout(1)

            # For debugging, log that the connection was received.
            print("Connection recieved: ", [user, nick])

            # Send out the initial connection information
            con.send(b':irc.ssg 001' + nick.encode('utf-8') + b':Welcome to the Internet Relay Network \r\n')
        except socket.timeout:
            # There was no one waiting.
            pass

        # During the loop we'll mark any users that have DC'ed.
        drop_users = []

        # We now have all the users. Let us continue with the interactions for each:
        for i, user in enumerate(users):
            # if the socket times out we continue, if the user id disconnected, we note it and continue.
            try:
                # Multiple lines could have been recieved while we were interacting with other users.
                # So we'll need to split the line and iterate over the result.
                lines = user['con'].recv(4096).decode('utf-8').split('\r\n')
            except socket.timeout:
                # Nothing new.
                continue
            except OSError:
                # connection was dropped
                drop_users.append(i)
                continue

            for line in lines:
                # turn the line into command + arguments
                command = line.split(' ')
                arguments = command[1:]
                command = command[0].lower()

                # For debugging, print the command and arguments.
                print(command, arguments)

                # Any command that isn't here we are skipping because they aren't necessary to show the basic operation.
                if command in ['nick', 'join', 'privmsg', 'part', 'quit']:
                    # Update users' Nick name. Pretty simple.
                    if command == 'nick':
                        user['nick'] = arguments[0]
                        user['con'].send(b'Nick has been updated.')

                    # Join the user to a channel by adding that channel to their list of channels.
                    elif command == 'join':
                        user['channels'].append(arguments[0])

                    # Received a message.
                    elif command == 'privmsg':
                        # Rejoin the message prefaced by the user's name.
                        message = user['nick'] + ' '.join(arguments[1:])

                        # Now iterate over all the users and find any that are in the channel the user is sending it to.
                        for rec_user in users:
                            if arguments[0] in rec_user['channels']:
                                # If the user is in the channel, send them the message.
                                rec_user['con'].send(message.encode('utf-8'))

                    # User has requested to leave a channel.
                    elif command == 'part':
                        user['channels'].pop(user['channels'].index(arguments[0]))

                    # User has terminated the connection
                    elif command == 'quit':
                        user['con'].close()
                        drop_users.append(i)

                else:
                    # Client tried to use a command that we have not implemented.
                    pass

            # Go through the list backwards.
            for user in drop_users[::-1]:
                users.pop(user)

    except KeyboardInterrupt:
        # Exit
        break
    except socket.timeout:
        # Expected
        pass
    except Exception as e:
        # Because you don't want silly errors crashing your super professional IRC server, capture all errors and print
        # the error message.
        print(e)

# Gracefully shutdown by closing the socket.
sock.close()
