# As usual with this project, keeping the imports to a minimum.
import socket
import sys

# To keep interactions to a minimum we are going to depend on CLI arguments. The user needs to pass all said arguments
# in. If they do not send at least 3 arguments (plus the initial call which is arg[0]) then exit.
if len(sys.argv) < 4:
    print("Called with 3 arguments: Server sender receiver (optional: port)")
    sys.exit(1)

# First argument is what server is going to be managing our SMTP request. This will only work with servers that allow
# anonymous connections. Which for most people means it won't work with any. Your organization may have an internal SMTP
# server that accepts anonymous requests originating from inside the network. Other wise your best bet is the smtp
# server created along with this project.
server = sys.argv[1]
# Second argument is who we are sending the email as.
sender = sys.argv[2]
# Third argument is who we are sending the email to.
receiver = sys.argv[3]
# If the user passes a fourth argument it should be the port. If not we default to the standard port.
if len(sys.argv) > 4:
    port = int(sys.argv[4])
else:
    port = 25

# Request the content from the user.
message = input('Enter your message. Blank line to conclude. \n') + '\n'

# Keep requesting it until the user passes two blank lines.
while '\n\n' not in message:
    message += input() + '\n'

# Request a socket.
con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Set a time out.
con.settimeout(1)
# Connect to the requested server.
con.connect((server, port))

# A quick little convenience method. Splits responses into the code and user readable information.
def split_line(line):
    try:
        return int(line[:3].decode('utf-8')), line[3:].decode('utf-8')
    except ValueError as e:
        print('Server sent malformed message: {}'.format(line))
        sys.exit(1)

# We are ready to do this. This process will consist of an opening message from the server and then 6 steps:
# 1. Introduce ourselves.
# 2. Let the server know we want to send an email.
# 3. Let the server know who we are sending the email to.
# 4. Let the server know we want to send the message body
# 5. The message body adding a the line with a single . to mark the end of the message.
# 6. In order to be compliant with the SMTP protocol you must request the server close your connection.

# Get the initial opening message
code, line = split_line(con.recv(1024))
if code == 220:  # 220 The server is ready
    print('Connected')
    print(line)
else:
    # Possible errors at this point:
    # 421 Service is unavailable due to a connection problem
    print('Error: {}'.format(code))
    print(line)
    sys.exit(code)

# 1. Introduce ourselves.
con.send(b'HELO [127.0.1.1]\r\n')
code, line = split_line(con.recv(1024))
if code == 250: # 250 Requested mail action okay completed
    print('Connection successful: '.fomrat(line))
else:
    # Possible errors at this point:
    # 421 Service is unavailable due to a connection problem
    # 500 Syntax error
    # 501 Syntax error in parameters or arguments
    # 504 Command parameter is not implemented
    print('Error: {}'.format(code))
    print(line)
    sys.exit(code)

# 2. Let the server know we want to send an email.
con.send('MAIL FROM:<{}>\r\n'.format(sender).encode('utf-8'))
code, line = split_line(con.recv(1024))
if code == 250: # 250 Requested mail action okay completed
    print('Building email on server...')
else:
    # Possible errors at this point:
    # 421 Service is unavailable due to a connection problem
    # 451 Aborted – Local error in processing
    # 452 Too many emails sent or too many recipients
    # 500 Syntax error
    # 501 Syntax error in parameters or arguments
    # 552 Exceeded storage allocation
    print('Error: {}'.format(code))
    print(line)
    sys.exit(code)

# 3. Let the server know who we are sending the email to.
con.send('RCPT TO:<{}>\r\n'.format(receiver).encode('utf-8'))
code, line = split_line(con.recv(1024))
if code == 250: # 250 Requested mail action okay completed
    print('Recipient accepted')
elif code == 251: # 251 User not local will forward
    print('Recipient is not local, but the server will forward it.')
else:
    # Possible errors at this point:
    # 421 Service is unavailable due to a connection problem
    # 450 User’s mailbox is unavailable
    # 451 Aborted – Local error in processing
    # 452 Too many emails sent or too many recipients
    # 500 Syntax error
    # 501 Syntax error in parameters or arguments
    # 503 Bad sequence of commands, or requires authentication
    # 550 Non-existent email address
    # 551 User not local or invalid address – relay denied
    # 552 Exceeded storage allocation
    # 553 Mailbox name invalid
    print('Error: {}'.format(code))
    print(line)
    sys.exit(code)

# 4. Let the server know we want to send the message body.
con.send(b'DATA\r\n')
code, line = split_line(con.recv(1024))
if code == 354: # 354 Start mail input
    print('Server is accepting message body')
else:
    # Possible errors at this point:
    # 421 Service is unavailable due to a connection problem
    # 451 Aborted – Local error in processing
    # 500 Syntax error
    # 501 Syntax error in parameters or arguments
    # 503 Bad sequence of commands, or requires authentication
    # 554 Transaction has failed
    print('Error: {}'.format(code))
    print(line)
    sys.exit(code)

# 5. The message body adding a the line with a single . to mark the end of the message.
con.send(message.encode('utf-8') + b'\r\n.\r\n')
code, line = split_line(con.recv(1024))
if code == 250: # 250 Requested mail action okay completed
    print('Server has accepted the message and queued it for delivery.')
else:
    # Possible errors at this point:
    # 421 Service is unavailable due to a connection problem
    # 451 Aborted – Local error in processing
    # 452 Too many emails sent or too many recipients
    # 500 Syntax error
    # 501 Syntax error in parameters or arguments
    # 503 Bad sequence of commands, or requires authentication
    # 554 Transaction has failed
    print('Error: {}'.format(code))
    print(line)
    sys.exit(code)

# 6. In order to be compliant with the SMTP protocol you must request the server close your connection.
con.send(b'QUIT\r\n')
code, line = split_line(con.recv(1024))
if code == 221: # 221 The server is closing its transmission channel
    print('Message sent')
else:
    # Possible errors at this point:
    # 500 Syntax error
    print('Error: {}'.format(code))
    print(line)

con.close()