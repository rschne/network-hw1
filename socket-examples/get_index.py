import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#now connect to the web server on port 80
# - the normal http port
s.connect(("stackoverflow.com", 80))
#s.settimeout(2)
#s.send(bytes('GET / HTTP/1.1\r\nHost: stackoverflow.com\r\nConnection: close\r\n\r\n', 'utf8'))
s.send(bytes('GET / HTTP/1.1\r\nHost: stackoverflow.com\r\nConnection: close\r\n\r\n', 'utf8'))
page = ''
while True:
	b = s.recv(1000)
	page += bytes.decode(b)
	if len(b) == 0: 
		print('Connection closed')
		break
s.close()

f = open('a.html', 'w')
f.write(page)
f.close()
