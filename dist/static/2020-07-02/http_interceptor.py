import socketserver
import socket
import sys

# Example Request
example_request = b'GET / HTTP/1.1\r\nUser-Agent: Wget/1.19.4 (linux-gnu)\r\nAccept: */*\r\nAccept-Encoding: identity\r\nHost: lunduke.com\r\nConnection: Keep-Alive\r\n\r\n'
example_response = b'HTTP/1.1 200 OK\r\nDate: Thu, 12 Mar 2020 20:38:47 GMT\r\nServer: Apache/2.4.18 (Ubuntu)\r\nLast-Modified: Thu, 12 Mar 2020 05:12:34 GMT\r\nETag: "26ee-5a0a1668a0bad"\r\nAccept-Ranges: bytes\r\nContent-Length: 9966\r\nVary: Accept-Encoding\r\nKeep-Alive: timeout=5, max=100\r\nConnection: Keep-Alive\r\nContent-Type: text/html\r\n\r\n<!doctype html>\n<html lang="en-US">\n  <head>\n    <title>Lunduke Journal</title>\n    <meta charset="utf-8" />\n    <meta name="generator" content="Hugo 0.62.2" />\n    <meta name="viewport" content="width=device-width, initial-scale=1" />\n    <meta name="author" content="Bryan Lunduke" />\n    <meta name="description" content=" " />\n    <link rel="stylesheet" href="https://lunduke.com/css/main.min.f90f5edd436ec7b74ad05479a05705770306911f721193e7845948fb07fe1335.css" />\n\n    <meta name="twitter:card" content="summary"/>\n<meta name="twitter:title" content="Lunduke Journal"/>\n<meta name="twitter:description" content=" "/>\n\n    <meta property="og:title" content="Lunduke Journal" />\n<meta property="og:description" content=" " />\n<meta property="og:type" content="website" />\n<meta property="og:url" content="https://lunduke.com/" />\n<meta property="og:updated_time" content="2020-03-11T02:07:00-08:00" />\n\n\n  </head>\n  <body>\n    <header class="app-header">\n      <a href="https://lunduke.com/"><img class="app-header-avatar" src="https://lunduke.com/justme.png" alt="Bryan Lunduke" /></a>\n      <h2>Lunduke Journal</h2>\n      <p> </p>\n      <div class="app-header-social">\n        \n      </div>\n\t  Video<br>\n\t  <a href="https://open.lbry.com/@Lunduke:e">LBRY</a> - <a href="https://www.youtube.com/bryanlunduke">YouTube</a>\n\t  <br><br>\n\t  Audio Podcast<br>\n\t  <a href="http://vault.lunduke.com/LundukeShowMP3.xml">RSS Feed</a> - <a href="https://podcasts.apple.com/us/podcast/the-lunduke-show/id1465523928">iTunes</a><br>\n\t  <a href="https://play.google.com/music/m/I3eptvmuqocsoc5qmqj4xcs2dcm?t=The_Lunduke_Show">Google Play</a> - <a href="https://open.spotify.com/show/5onwMz4y48zrM4s5WS20bT">Spotify</a>\n\t  <br><br>\n\t  Read The Articles<br>\n\t  <a href="https://lunduke.com/index.xml">RSS Article Feed</a><br>\n\t  <br>\n\t  <a href="https://lunduke.com/pages/about/">About Lunduke</a> - <a href="https://lunduke.com/pages/bbs/">BBS</a>\n\t  <br>\n\t  <a href="https://lunduke.com/pages/codeofconduct/">Lunduke Code of Conduct</a>\n\t  <br>\n\t  <a href="https://the-lunduke-store.myshopify.com/collections/all">The Lunduke Store</a>\n\t  <br><br>\n\t  <a href="https://www.patreon.com/bryanlunduke">Support The Lunduke Journal</a>\n    </header>\n    <main class="app-container">\n      \n  <article>\n    <h1>Lunduke Journal -- Computing. Old & New.</h1>\n    <ul class="posts-list">\n      \n        <li class="posts-list-item">\n          <a class="posts-list-item-title" href="https://lunduke.com/posts/2020-03-10/">Microsoft Windows 1.04 - Best OS... ever?</a>\n          <span class="posts-list-item-description">\n            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-clock">\n  <title>clock</title>\n  <circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline>\n</svg> 8 min read -\n            Mar 11, 2020\n          </span>\n        </li>\n      \n        <li class="posts-list-item">\n          <a class="posts-list-item-title" href="https://lunduke.com/posts/2020-03-9-b/">Open Source Initiative bans co-founder, Eric S Raymond</a>\n          <span class="posts-list-item-description">\n            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-clock">\n  <title>clock</title>\n  <circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline>\n</svg> 9 min read -\n            Mar 9, 2020\n          </span>\n        </li>\n      \n        <li class="posts-list-item">\n          <a class="posts-list-item-title" href="https://lunduke.com/posts/2020-03-06/">The Best Linux Marketing Campaigns.  Ever.</a>\n          <span class="posts-list-item-description">\n            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-clock">\n  <title>clock</title>\n  <circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline>\n</svg> 5 min read -\n            Mar 6, 2020\n          </span>\n        </li>\n      \n        <li class="posts-list-item">\n          <a class="posts-list-item-title" href="https://lunduke.com/posts/2020-03-05/">Microsoft BASIC for TRS-80 Model 100 - Best OS... ever?</a>\n          <span class="posts-list-item-description">\n            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-clock">\n  <title>clock</title>\n  <circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline>\n</svg> 10 min read -\n            Mar 5, 2020\n          </span>\n        </li>\n      \n        <li class="posts-list-item">\n          <a class="posts-list-item-title" href="https://lunduke.com/posts/2020-03-04-b/">From 2012: How removing 386 support in Linux will destroy the world</a>\n          <span class="posts-list-item-description">\n            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-clock">\n  <title>clock</title>\n  <circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline>\n</svg> 3 min read -\n            Mar 4, 2020\n          </span>\n        </li>\n      \n        <li class="posts-list-item">\n          <a class="posts-list-item-title" href="https://lunduke.com/posts/2020-03-04/">Without a GUI - How to Live Entirely in a Terminal</a>\n          <span class="posts-list-item-description">\n            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-clock">\n  <title>clock</title>\n  <circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline>\n</svg> 8 min read -\n            Mar 4, 2020\n          </span>\n        </li>\n      \n        <li class="posts-list-item">\n          <a class="posts-list-item-title" href="https://lunduke.com/posts/2020-03-03/">The Beauty of a Static Website with Hugo</a>\n          <span class="posts-list-item-description">\n            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-clock">\n  <title>clock</title>\n  <circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline>\n</svg> 7 min read -\n            Mar 3, 2020\n          </span>\n        </li>\n      \n        <li class="posts-list-item">\n          <a class="posts-list-item-title" href="https://lunduke.com/posts/2020-03-02/">Ask Lunduke - Mar 2, 2020 - The UNIX Wars</a>\n          <span class="posts-list-item-description">\n            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-clock">\n  <title>clock</title>\n  <circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline>\n</svg> 3 min read -\n            Mar 2, 2020\n          </span>\n        </li>\n      \n        <li class="posts-list-item">\n          <a class="posts-list-item-title" href="https://lunduke.com/posts/2020-03-01/">Two Months Without Social Media</a>\n          <span class="posts-list-item-description">\n            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-clock">\n  <title>clock</title>\n  <circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline>\n</svg> 4 min read -\n            Mar 1, 2020\n          </span>\n        </li>\n      \n        <li class="posts-list-item">\n          <a class="posts-list-item-title" href="https://lunduke.com/posts/2020-02-26-b/">Lunduke\xe2\x80\x99s Theory of Computer Mockery \xe2\x80\x94 no technology is sacred</a>\n          <span class="posts-list-item-description">\n            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-clock">\n  <title>clock</title>\n  <circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline>\n</svg> 4 min read -\n            Feb 26, 2020\n          </span>\n        </li>\n      \n    </ul>\n    \n\n<ul class="pagination">\n  \n  \n  <li class="page-item active">\n    <a class="page-link" href="https://lunduke.com/">\n      1\n    </a>\n  </li>\n  \n  <li class="page-item">\n    <a class="page-link" href="https://lunduke.com/page/2/">\n      2\n    </a>\n  </li>\n  \n  <li class="page-item">\n    <a class="page-link" href="https://lunduke.com/page/3/">\n      3\n    </a>\n  </li>\n  \n  <li class="page-item">\n    <a class="page-link" href="https://lunduke.com/page/4/">\n      4\n    </a>\n  </li>\n  \n  <li class="page-item">\n    <a class="page-link" href="https://lunduke.com/page/5/">\n      5\n    </a>\n  </li>\n  \n  \n  <li class="page-item">\n    <a class="page-link" href="https://lunduke.com/page/2/">\n      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-arrow-right">\n  <title>arrow-right</title>\n  <line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline>\n</svg>\n    </a>\n  </li>\n  \n</ul>\n\n\n\n  </article>\n\n    </main>\n  </body>\n</html>\n'


class HttpHandler(socketserver.BaseRequestHandler):
    def handle(self):
        raw_request = self.request.recv(4096)
        parts = raw_request.split(b'\r\n')
        
        raw_request = raw_request.replace(b'localhost:8080',b'lunduke.com')
        print('Request: {}'.format(raw_request))
        
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(10)
        client.connect(('51.158.66.5', 80))
        client.send(raw_request)
        
        response = b''
        size = -1
        while len(response) != size:
            size = len(response)
            try:
                response += client.recv(4096)
            except socket.timeout:
                pass
        print('Response: {}'.format(response))
        
        client.close()
        self.request.sendto(response, self.client_address)

if __name__ == '__main__':
    host, port = '', 8080
    server = socketserver.ThreadingTCPServer((host, port), HttpHandler)
    print("Starting server")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        sys.exit(0)
