import socket

# Request a TCP Socket.
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Allow us to re-use the same port quickly.
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind to any traffic coming in on port 8025. We are using this port as you need special permissions for port 25.
sock.bind(('0.0.0.0', 8025))
# Finally listen to that port for an incoming connection.
sock.listen(1)

# Loop forever.
while True:
    # I have put it all inside of a try block here so that you can gracefully shut down the server on keyboard escape.
    try:
        # First we wait for a connection
        con, addr = sock.accept()

        # Send out the initial connection information
        con.send(b'220 localhost Studio Sleepy Giraffe MAIL Service, Version: 1.3.3.7 \r\n')

        line = con.recv(1048).decode('utf-8')

        # All SMTP commands are 4 characters long, so we can just lop off these 4 characters to get our command.
        # SMTP is case insensative, so we'll cast this to upper case to simplify comparing later.
        command = line[:4].upper()
        # The rest of the string is the arguments, so we can just lop those into the arguments variable.
        arguments = line[4:]

        # These are the "data tables" so to speak. They are the variables that hold the pieces of information we are
        # interested in. In a proper implementation of SMTP there would be a lot more to handle things like encryption
        # and large binary files and various othere MIME types. We are going for the simplest possible implementation
        # here so these are good enough.
        sender = ''
        receiver = ''
        message = ''
        while command != 'QUIT':
            # Print it out so we can see what's happening.
            print(command, arguments)
            # Commands not implemented here: SEND, SOML, SAML, VRFY, EXPN, HELP, TURN
            # We are skipping them because they aren't necessary to show the basic operation.
            if command in ['HELO', 'MAIL', 'RCPT', 'DATA', 'RSET', 'NOOP']:
                # The hello command is used by the sender to identify themselves. In this case we don't care, but you
                # could use the information provided here to decide whether or not to communicate with the sender. You
                # would want to do some form of additional validation, like take their IP, do a reverse lookup and
                # validate that they are who they say they are. In our case we'll just say hello back.
                if command == 'HELO':
                    con.send(b'250-localhost SSG hello\r\n')

                # MAIL signifies that the sender is getting ready to send an email. This initiates the mail transaction.
                # A more polished implementation of an SMTP server would be stateful and this command would push the
                # server into a MAIL state. We are keeping this simple so we'll just extract the inforation we need and
                # carry on our merry way.
                elif command == 'MAIL':
                    # The sender will start after the first angle bracket.
                    start = arguments.find('<') + 1
                    # The address finishes at the end of the first closing angle bracket.
                    end = arguments.find('>')
                    # use those number to extract the sender.
                    sender = arguments[start:end]
                    # Let the client know all is well.
                    con.send('250 {}....Sender OK\r\n'.format(sender).encode('utf-8'))

                # RCPT, or recipient, is used to identify an individual recipient of the mail data. If you have multiple
                # recipients in mind you would need to call this command multiple times. For our purposes though we are
                # only implementing a single recipient.
                elif command == 'RCPT':
                    # Like sender, the email is between the angle brackets.
                    start = arguments.find('<') + 1
                    end = arguments.find('>')
                    # Extract the recipient
                    receiver = arguments[start:end]
                    # Let the client know that they can continue.
                    con.send('250 {}\r\n'.format(sender).encode('utf-8'))

                # DATA initializes the body of the message. The following lines, no matter how numerous, are all to be
                # treated as the body of the message. Only when we receive a line with a single period on it,
                # <CRLF>.<CRLF>, do we conclude that the body has been completely transferred. An important note here is
                # that when you finish this portion of the process the message will be sent. If the server was stateful
                # that would mean this command takes the server into the 'data' state where everything goes into the
                # message and when it is done returns it to the default state, OUTSIDE of the 'mail' state.
                elif command == 'DATA':
                    # Let the client know that we have moved into the data state and will be waiting for the terminator.
                    con.send(b'354 Start mail input; end with <CRLF>.<CRLF>\r\n')

                    # While the message body does not contain the terminator, continue.
                    while '\r\n.\r\n' not in message:
                        message += con.recv(1048).decode('utf-8')

                    # Lop off the terminator now that we have finished.
                    message = message[:-3]

                    # Let the client know everything is golden and the message is queued for delivery.
                    con.send(b'250 Queued mail for delivery\r\n')

                    # We aren't going to bother with upstream forwarding or anything like that. For our little example
                    # simply saving the file where the server is running is good enough. A more proper way to do this
                    # would be to save it to the /var/spool/mail/user or /var/mail/user. But you probably don't have
                    # permissions setup correctly for those folders, or you might be on a windows machine which wouldn't
                    # have those folders.
                    open('{} to {}.txt'.format(sender, receiver), 'w').write(message)

                # RSET, or reset, clears all the data prepared to send. Like it suggests, it resets.
                elif command == 'RSET':
                    sender = ''
                    receiver = ''
                    message = ''
                    con.send(b'250 Tables cleared\r\n')
            else:
                # Client tried to use a command that we have not implemented.
                con.send(b'504 Command parameter is not implemented\r\n')

            # Prepare the next command and arguments set.
            line = con.recv(1048).decode('utf-8')
            command = line[:4].upper()
            arguments = line[4:]

        # Let the user know we have terminated the connection.
        con.send(b'221 Service closing transmission channel\r\n')

        # Close the connection.
        con.close()

    except KeyboardInterrupt:
        # Exit
        break
    except Exception as e:
        # Because you don't want silly errors crashing your super professional smtp server, capture all errors and print
        # the error message.
        print(e)

# Gracefully shutdown by closing the socket.
sock.close()

