import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost',4000))
print(s.recv(4096))
s.close()

# Before you run this script run:
# netcat -l -p 4000
# That will start up a socket server on your local machine. Then run this script on your local machine or on a seperate
# computer replacing 'localhost' with the IP of the machine running netcat. You will then be able to type whatever you
# want into the netcat dialog and it will be sent over to the machine running this script. Think of what you could do
# with the ability to arbitrarily receive data from any computer.

# Note: This script will only print out the first line of text you send. Netcat will wait for you to finish a line, then
# when you press enter netcat will queue that up and send it and then wait for more from you. But that one transaction,
# up to 4096 characters, is all this script will listen to. The making of a while loop is left as an exercise for the
# reader.