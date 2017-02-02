# http://stackoverflow.com/search?q=HTTP
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#now connect to the web server on port 80
# - the normal http port
target = 'yahoo.com'
s.connect((target, 80))
s.settimeout(2)
s.send(bytes('GET /search?q=HTTP HTTP/1.1\r\nHost: %s\r\nConnection: close\r\n\r\n'  % target, 'utf8'))
page = ''
while True:
	print('here')
	bytes = s.recv(1000)
	page = page + str(bytes);
	#print(bytes)
	if len(bytes) == 0: 
		print('Connection closed')
		break
s.close()
f = open('a.html', 'w')
f.write(page)
f.close()

