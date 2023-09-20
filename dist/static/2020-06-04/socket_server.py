import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('',4000)) # note you are passing a tuple.
s.listen(1)
connection, address = s.accept() # this will wait for a connection
connection.send(b'Hello world!')
connection.close()

# Run this script and then in a seperate terminal window run
# netcat localhost 4000
# or on a separate computer replace localhost with your host computer's IP. This will send the byte string Hello world!
# over the the network or loop back to the computer running netcat. Try changing the byte string to what ever you want
# and imagine the possibilities.