from dns_methods import create_questions, create_header, process_header
from dns_methods import process_questions, process_resource_record
import socket

# Get the header. Request ID can be anything under 65535.
# As I understand it, rd is required incase the first server you contact does
# not have the name you are looking for. In which case it then proceeds to
# request it from the next server and so on until one is found or a server 
# refuses to do a recusive call.
# qdcount: How many questions we will be sending. For now, 1
# The result, request, is a byte string we will add to as we go.
request = create_header(request_id=31415, rd=1, qdcount=1)

# Next get the questions in the binary format.
url = 'txt.studiosleepygiraffe.com'
request += create_questions(url, 'TXT')

# Create a socket with UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Connect to Open DNS, or local host depending on what you are testing against right now.
s.connect(('208.67.222.222', 53))
#s.connect(('localhost', 8053))

# Send the request to the Open DNS server
s.send(request)

# Resceive the response
response = s.recv(1024)

# Pull out the number of questions and the number of answers, all we need. Drop the rest.
# request_id, qr, opcode, aa, tc, rd, ra, z, rcode, qdcount, ancount, nscount, arcount
_, _, _, _, _, _, _, _, _, qdcount, ancount, _, _ = process_header(response[:12])

# This is primarily to find where the questions finish.
_, resource_start = process_questions(response, qdcount)

# Prepare a list for storing results
results = []

# Loop through the number of results.
for answer in range(ancount):
    # Extract the record and append it.
    result, resource_start = process_resource_record(response, resource_start)
    results.append(result)

# Print the results
print(results)
