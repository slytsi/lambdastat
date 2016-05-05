import socket

HOST = '192.168.1.26'    # The remote host
PORT = 4998              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall('sendir,1:1,15,37993,1,1,246,160,20,60,20,60,20,60,20,20,20,60,20,20,20,60,20,60,20,160,20,60,20,60,20,20,20,60,20,20,20,20,20,20,20,20,20,721,320,160,20,60,20,60,20,60,20,20,20,60,20,20,20,60,20,60,20,160,20,60,20,60,20,20,20,60,20,20,20,20,20,20,20,20,20,3700,\r,\l')
data = s.recv(1024)
s.close()
print 'Received', repr(data)
