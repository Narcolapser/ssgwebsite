from dns_methods import process_header, process_questions, create_header, create_resource_record
import socketserver
import sys

# My little DNS database. You can add more records here to your liking.
records = {'studiosleepygiraffe.com': {'A': '96.2.162.67'},
           'txt.studiosleepygiraffe.com': {'TXT': b'\x1bThis is an example message.'}}

# Convert the records from the human readable format above into a four bytes.
def ipv4_to_bytes(ip):
    result = b''
    for part in ip.split('.'):
        val = int(part)
        result += bytes([val])
    return result

# I'm using a class to help keep this code brief. I hand really hoped to keep it
# strictly sockets, but this is pretty close. UDP does some weird things in the
# background that I didn't want to deal with.
class DNSHandler(socketserver.BaseRequestHandler):
    # On each request this method gets called to process it.
    def handle(self):
        # Exract the connection.
        con = self.request[1]
        
        # Extract the request stripping off extra white space.
        request = self.request[0].strip()
        print('Recieved a request from: {}'.format(request))
        
        # Process the header to get the parts we need.
        request_id, qr, opcode, aa, tc, rd, ra, z, rcode, qdcount, ancount, nscount, arcount = process_header(request)
        print('Asking {} question(s).'.format(qdcount))

        # Get the questions to answer.
        questions, pointer = process_questions(request, qdcount)
        answers = []
        
        # Iterate over each question attempting to answer it.
        for question in questions:
            print('"{}" record for {}'.format(question[1], question[0]))
            data = None
            
            # Check that the address is in our database.
            if question[0] in records:
                # If it is, check that the address has the requested record type
                if question[1] in records[question[0]]:
                    # If it is an address record get the IP.
                    if question[1] == 'A':
                        data = ipv4_to_bytes(records[question[0]][question[1]])
                    # other wise just push whatever binary we have for it.
                    else:
                        data = records[question[0]][question[1]]

            # If the request was not in the database the normal next step would
            # be to search recusively, but that's beyond the scope of this
            # little example. So we'll just return that it was not found. 
            if not data:
                print('But I don\'t know it.')
                continue

            # Add the answer we found to the list.
            answers.append(create_resource_record(question[0], question[1], question[2], 0, data))

        # Create a new header for the response.
        response = create_header(request_id=request_id, qdcount=qdcount, ancount=len(answers))
        
        # We can save some effort by just copying the questions from the request
        # over into the response.
        response += request[12:pointer]
        
        # Concatenate all of the answers together and we are done.
        response += b''.join(answers)

        # Send reply to requestor.
        con.sendto(response, self.client_address)


# Setup the server.
if __name__ == '__main__':
    # UDP does not appear to use a binding address. 
    # We'll use port 8053 so as to avoid the elevated permissions needed to
    # access restricted ports like 53 (any port below 1024).
    host, port = '', 8053
    
    # Create the server.
    server = socketserver.ThreadingUDPServer((host, port), DNSHandler)
    print("Starting server")
    
    try:
        #Run it forever.
        server.serve_forever()
    except KeyboardInterrupt:
        #When it is stopped with a ctl-c, shut it down gracefully.
        server.shutdown()
        sys.exit(0)
