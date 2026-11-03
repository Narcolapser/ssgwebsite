import socket

# Our little web page to serve. You could replace this with any HTML string and host a little toy website if you wanted.
page = """
<html>
    <title>Example HTTP Server from scratch!</title>
    <p>You requested: {}</p>
    <p>Form Content: {}</p>
    <form action="/form.html" method="post">
        <label for="text_input">Enter some text</label>
        <input type="text" id="text_input" name="text_input" value="Default"></input>
        <input type="submit" value="Submit">
    </form>
</html>
"""

# Request a TCP Socket.
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Allow us to re-use the same port quickly.
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind to any traffic coming in on port 8080. We are using this port as you need special permissions for port 80.
sock.bind(('0.0.0.0', 8080))
# Finally listen to that port for an incoming connection.
sock.listen(1)

# Loop forever.
while True:
    # I have put it all inside of a try block here so that you can gracefully shut down the server on keyboard escape.
    try:
        # First we wait for a connection
        con, addr = sock.accept()

        # Then recieve the request. For our purposes we can assume the request will never be bigger than 4k.
        raw_request = con.recv(4096)

        # Split the request into parts so we can get the request line, the headers, and the body.
        parts = raw_request.split(b'\r\n')

        # Request line is always first.
        request = parts[0]

        # Break the request line into it's peices.
        method, uri, http_version = request.split(b' ')
        # Print the method and uri so we can see them.
        print(method, uri)

        # Next the headers. We don't actually use them, but we need to process them out of the way.
        headers = []
        i = 1
        #Go until we hit a blank line, that will mark the double line break between the headers and the body.
        while i < len(parts) and parts[i] != b'':
            headers.append(parts[i])
            i += 1
        # The body is all the lines that are left.
        body = b'\n'.join(parts[i:])

        # Alright, we've got what we need. Now lets construct the response.
        response = ''

        # These are the same regardless of GET or POST
        headers = [
            # What the type of content we are returning.
            'Content-Type: text/html',
            # A little bit about the server. This can be what ever you want it to be.
            'Server: StudioSleepyGiraffe/1.0 (Python)',
        ]

        # We are only going to concern ourselves with two types of requests, GET and POST.
        if method == b'GET':
            # For a GET request we are just simply saying things worked.
            status_line = 'HTTP/1.1 200 OK'
            # The response is going to be our pre-canned page. adding the requested URI to show a little bit of dynamic
            # behavior that could be futher expanded.
            resp_body = page.format(uri.decode('utf-8'), 'None in a GET request.')
            # Add the content length header now that we can calculate it.
            headers.append('Content-Length: ' + str(len(resp_body)))

        elif method == b'POST':
            # For a POST request we sign that the form request has been received.
            status_line = 'HTTP/1.1 201 Created'
            # Construct the response using the form data as a further dynamic behavior.
            resp_body = page.format(uri.decode('utf-8'), body.decode('utf-8'))
            # Add the content length header now that we can calculate it.
            headers.append('Content-Length: ' + str(len(resp_body)))

        # Template of the response. Pretty simple to work with. First the status line, then the headers, then the body.
        # The first two seperated by a new line and the last two seperated by two new lines.
        response_template = '{status_line}\r\n{headers}\r\n\r\n{body}'
        # And punch in the values.
        response = response_template.format(status_line=status_line,
                                            headers='\r\n'.join(headers),
                                            body=resp_body)

        # Convert the response into raw bytes for transit.
        resp_bytes = response.encode('utf-8')

        # Just so we can see what's going.
        print(response)

        # Send the response.
        con.send(resp_bytes)

        # Close the connection.
        con.close()
    except KeyboardInterrupt:
        # Exit
        break
    except Exception as e:
        # Because you don't want silly errors crashing your super professional web server, capture all errors and print
        # the error message.
        print(e)

# Gracefully shutdown by closing the socket.
sock.close()
