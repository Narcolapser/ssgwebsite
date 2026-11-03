import socket
# This is included simply to do some html parsing later as html parsing is not in the scope of this project. This can be
# removed without changing the function of the program, you'll just have to print and read raw html instead.
from bs4 import BeautifulSoup

# Ask the user for the URL that we will request.
url = input('Please enter url (blank to exit): ')

# While the user hasn't passed us an empty url
while url != '':

    # If the url contains a forward slash we have been passed a full path, e.g. "www.studiosleepygiraffe.com/blog"
    if '/' in url:
        # split that url into parts so we can extract the domain name of the website.
        parts = url.split('/')

        # The first part is the domain name.
        host = parts[0]

        # The rest of it can be put back together to create the specific path.
        path = '/' + '/'.join(parts[1:])

    # If the url does not contain a forward slash the user sent us a just the domain, e.g. "www.studiosleepygiraffe.com"
    else:
        # In this case the provided url is the domain.
        host = url
        # and the path is root
        path = '/'

    # NOTE: This is simplified for example purposes as usual. The scenario where the user sends
    # "http://studiosleepygiraffe.com" would cause this to break. But I'm not concerned with that case right now since
    # the purpose here is to talk about how http clients work not how urls are parsed.

    # Header information. Part meta data, part negotiation of how to communicate.
    headers = {
        # User agent tells the webserver who is talking. Basically you identifying yourself.
        'User-Agent': 'StudioSleepyGiraffeCLIBrowser',
        # Tell the webserver what types of content you'll accept. In this case, anything.
        'Accept': '*/*',
        # Tell the host what host you are trying to contact. This is useful in the case of redirects.
        'Host': host
    }

    # Construct the first line. This is simple in this case because we are restricting two of the values. We are only
    # going to be making GET requests and we are only going to work with HTTP/1.1.
    req = 'GET {path} HTTP/1.1\r\n'.format(path=path)

    # This converts the list of headers into strings the format expected. This format goes WAY back. RFC 822, the
    # second part of SMTP you could say. HTTP was offecially specified in 1997, but SMTP headers on which HTTP headers
    # are based was specified in 1982. The design is quite simple:
    # key:value
    # That's it. A string with a key and a value seperated by a colon. You can actually do multi-lined headers as well
    # as long as the first character of the new line starts with a white space character then it is assumed that the
    # line is part of the previous header statement. Further reading: https://tools.ietf.org/html/rfc822#section-3.1
    str_headers = ['{}: {}'.format(header, headers[header]) for header in headers]

    # Finally join those headers with new lines, using the archaic new line \r\n. Then you tack on two new lines to
    # signal the end of the headers. If this was a post or put method then we would add a body after that.
    req += '\r\n'.join(str_headers) + '\r\n\r\n'

    # So you can see what the request that was just made actually looks like
    print(req)
    print(len(req))

    # Open a socket with TCP.
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Set max timeout to 2 seconds
    server.settimeout(2)
    # Connect to our requested host on the standard http port, 80
    server.connect((host, 80))
    # Finally convert the request string from above into raw bytes and send it off to the host server.
    server.send(req.encode('utf-8'))

    # Headers aren't usually longer than 1000 characters or so. This is garunteed to get all of the header section of
    # the response.
    response = server.recv(4096)

    # Next find the end of the header section, as before two line breaks marks the end.
    end_headers = response.find(b'\r\n\r\n')
    print(end_headers)

    # Now that we know where the headers end, clip the string there and then split the headers to seperate lines.
    response_headers = response[:end_headers].split(b'\r\n')

    # Technically the first line isn't a header, it's the status line. we'll just pull that one out of the list.
    status_line = response_headers[0]
    response_headers = response_headers[1:]

    # Now that we have the status line it has some important information for us. So we will split it up:
    parts = status_line.split(b' ')
    # First part is the HTTP version.
    http_version = parts[0].decode('utf8')
    # Second part is the status code, what we are really interested in.
    status_code = parts[1].decode('utf8')
    # Last part is a human readable status reason. This could have spaces in it so we have to rejoin it.
    status_reason = (b' '.join(parts[2:])).decode('utf8')

    # If it is not a 2xx status_code we failed so far as we are concerned. Reloop. A more through client would
    # automatically follow redirects. That is left as an exercise for the reader.
    if status_code[0] != '2':
        print('Failure: {} - {}'.format(status_code, status_reason))
        # Prepare the next request.
        url = input('Please enter url (blank to exit): ')
        continue

    # Now that we know we are working with a good response, lets convert the rest of the headers:
    headers = {}
    for header in response_headers:
        # As said above, headers are just key value pairs seperated by a colon
        parts = header.split(b':')
        # Key is the first part.
        key = parts[0].decode('utf-8')
        # The value could have a colon in it, like for a date, so we must rejoin it.
        value = (b':'.join(parts[1:]).decode('utf-8'))
        # Finally save the value
        headers[key] = value

    # Now that we've got all the headers, we can find out how long our payload is:
    content_length = int(headers['Content-Length'])

    # We know how long body is, we know how much we've already received, from that we can figure out how much is left.
    # The content-length does not include the header section or the separator, those we must subtract those out.
    content_left = content_length - (len(response) - (end_headers + 2))

    # Fetch the remaining content. In a normal enviorment it would be recommend to do this in a loop with smaller
    # chunks. However, this is good enough for our purposes.
    response += server.recv(content_left)

    # Finally extract the body:
    body = response[end_headers + 2:].decode('utf-8')

    # The beautifulsoup step is included to pretty print the HTML. It can be removed to make the script runable with 
    # only vanilla python.
    soup = BeautifulSoup(body)
    print(soup.prettify())

    # Prepare the next request.
    url = input('Please enter url (blank to exit): ')
