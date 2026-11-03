''' Sample 1:
Upward: b'CAP LS\r\nNICK toben\r\nUSER toben toben localhost :toben\r\n'
Downward: b':irc.example.net 001 toben :Welcome to the Internet Relay Network toben!~toben@172.17.0.1\r\n:irc.example.net 002 toben :Your host is irc.example.net, running version ngircd-18 (x86_64/pc/linux-gnu)\r\n:irc.example.net 003 toben :This server has been started Thu May 07 2020 at 20:38:40 (UTC)\r\n:irc.example.net 004 toben irc.example.net ngircd-18 aciorswx biIklmnoOPstvz\r\n:irc.example.net 005 toben RFC2812 IRCD=ngIRCd CASEMAPPING=ascii PREFIX=(ov)@+ CHANTYPES=#&+ CHANMODES=bI,k,l,imnPst CHANLIMIT=#&+:10 :are supported on this server\r\n:irc.example.net 005 toben CHANNELLEN=50 NICKLEN=9 TOPICLEN=490 AWAYLEN=127 KICKLEN=400 PENALTY :are supported on this server\r\n:irc.example.net 251 toben :There are 1 users and 0 services on 1 servers\r\n:irc.example.net 254 toben 1 :channels formed\r\n:irc.example.net 255 toben :I have 1 users, 0 services and 0 servers\r\n:irc.example.net 265 toben 1 1 :Current local users: 1, Max: 1\r\n:irc.example.net 266 toben 1 1 :Current global users: 1, Max: 1\r\n:irc.example.net 250 toben :Highest connect'
Upward: b'MODE toben +i\r\n'
Downward: b'ion count: 2 (10 connections received)\r\n:irc.example.net 375 toben :- irc.example.net message of the day\r\n:irc.example.net 372 toben :- **************************************************\r\n:irc.example.net 372 toben :- *             H    E    L    L    O              *\r\n:irc.example.net 372 toben :- *  This is a private irc server. Please contact  *\r\n:irc.example.net 372 toben :- *  the admin of the server for any questions or  *\r\n:irc.example.net 372 toben :- *  issues.                                       *\r\n:irc.example.net 372 toben :- **************************************************\r\n:irc.example.net 372 toben :- *  The software was provided as a package of     *\r\n:irc.example.net 372 toben :- *  Debian GNU/Linux <http://www.debian.org/>.    *\r\n:irc.example.net 372 toben :- *  However, Debian has no control over this      *\r\n:irc.example.net 372 toben :- *  server.                                       *\r\n:irc.example.net 372 toben :- **************************************************\r\n:irc.example.net'
Downward: b' 372 toben :- *  Run your own server anywhere that Docker runs *\r\n:irc.example.net 372 toben :- *                                                *\r\n:irc.example.net 372 toben :- *  At bash console: docker run -d carver/ngircd  *\r\n:irc.example.net 372 toben :- *  More Docker info at www.docker.io             *\r\n:irc.example.net 372 toben :- **************************************************\r\n:irc.example.net 376 toben :End of MOTD command\r\n:toben!~toben@172.17.0.1 MODE toben :+i\r\n'
Upward: b'PING irc.example.net\r\n'
Downward: b':irc.example.net PONG irc.example.net :irc.example.net\r\n'
Upward: b'JOIN #ssg\r\n'
Downward: b':toben!~toben@172.17.0.1 JOIN :#ssg\r\n:irc.example.net 353 toben = #ssg :@toben\r\n:irc.example.net 366 toben #ssg :End of NAMES list\r\n'
Upward: b'MODE #ssg\r\n'
Downward: b':irc.example.net 324 toben #ssg +\r\n:irc.example.net 329 toben #ssg 1588884440\r\n'
Upward: b'WHO #ssg\r\n'
Downward: b':irc.example.net 352 toben #ssg ~toben 172.17.0.1 irc.example.net toben H@ :0 toben\r\n:irc.example.net 315 toben #ssg :End of WHO list\r\n'
Upward: b'MODE #ssg b\r\n'
Downward: b':irc.example.net 368 toben #ssg :End of channel ban list\r\n'
Upward: b'PRIVMSG #ssg :hello\r\n'
Upward: b'PRIVMSG #ssg :world\r\n'
Upward: b'QUIT :leaving\r\n'
Downward: b':irc.example.net NOTICE toben :Connection statistics: client 0.2 kb, server 2.9 kb.\r\nERROR :"leaving"\r\n'
'''


import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('localhost', 6668))
s.listen(1)
client, addr = s.accept()
client.settimeout(1)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.settimeout(1)
server.connect(('localhost', 6667))

while True:
    try:
        upward = client.recv(1024)
        if upward != b'':
            print('Upward: {}'.format(upward))
        server.send(upward)
    except KeyboardInterrupt:
        break
    except:
        pass
        # print('nothing to pass up')
    try:
        downward = server.recv(1024)
        if downward != b'':
            print('Downward: {}'.format(downward))
        client.send(downward)
    except KeyboardInterrupt:
        break
    except:
        pass
        # print('nothing to pass down')
