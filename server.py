import socket, sys
from threading import Thread

HOST = ''
PORT = 4005

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket
print('Socket created')

try:
    s.bind((HOST, PORT)) #bind to port
except socket.error:
    print('Bind failed.')
    sys.exit() #quit on fail
     
print('Socket bind complete')

s.listen(10) #wait for connections
print('Socket listening')

allConn = []

def currentVersion():
    #find current version
    v = open('version.txt')
    version = v.read(1024)
    print('Current version is ' + version)
    v.close()
    return version

def updatedFiles():
    #check files that have been changed in this version
    updateFile = open('update.loc')
    changes = updateFile.readline(4096).split(':')
    version = changes[0]
    return changes[1]
    
def handler(conn):
    userVersion = conn.recv(1024).decode('utf-8')
    if(userVersion == version):
        needUpdate = version + ':uptodate'
    else:
        needUpdate = version + ':outdated'

    conn.send(bytes(needUpdate, 'utf-8'))
    changedFiles = updatedFiles()
    conn.send(bytes(changedFiles, 'utf-8'))

while 1:
    conn, addr = s.accept() #accept incoming connections
    version = currentVersion()
    allConn.append(conn) #add to connected sockets 
    print('Connected with ' + addr[0] + ':' + str(addr[1])) 
    Thread(target=handler, args=(conn,)).start() #start clientThread on new thread 

s.close() 
