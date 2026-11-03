import socket
import socketserver
import sys


class DNSHandler(socketserver.BaseRequestHandler):
    def handle(self):
        con = self.request[1]
        request = self.request[0].strip()
        print('Request: {}'.format(request))

        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.settimeout(10)
        client.connect(('208.67.222.222', 53))
        client.send(request)
        
        response = client.recv(4096)
        print('Response: {}'.format(response))
        
        client.close()
        con.sendto(response, self.client_address)

if __name__ == '__main__':
    host, port = '', 8053
    server = socketserver.ThreadingUDPServer((host, port), DNSHandler)
    print("Starting server")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        sys.exit(0)
