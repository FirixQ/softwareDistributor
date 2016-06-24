import socket

#connected to server and check for update

host = '127.0.0.1'
port = 4005

s = socket.socket()
s.connect((host, port))

print('Connected to update server')

#get version from file

v = open('version.txt')
version = v.read(1024)

#send to server

s.send(bytes(version, 'utf-8'))
needUpdate = s.recv(1024).decode('utf-8')

newVersion = needUpdate.split(':')[0]
updateRequired = needUpdate.split(':')[1]

#print output

if (updateRequired == 'uptodate'):
    print('Running latest version')

else:
    print('Update required to version ' + newVersion)

#update code here

changes = s.recv(4096).decode('utf-8')
print('Files to be changed: ' + changes)

#receive files
