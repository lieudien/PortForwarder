#!/usr/bin/python3

import selectors
import socket
import config

BUFLINE = 1024
myselect = selectors.DefaultSelector()
listenSocketForPort = {}
clientToServerDict = {}
serverToClientDict = {}

def onAccept(sock, mask):
    conn, addr = sock.accept()
    print("Received connect from {}".format(addr))
    conn.setblocking(False)
    myselect.register(conn, selectors.EVENT_READ, onRead)
    port = listenSocketForPort[sock]
    clientToServerDict[conn] = createConnection(config.PORT_HOSTS[port], port)
    serverToClientDict[clientToServerDict[conn]] = conn

def onRead(conn, mask):
    data = conn.recv(BUFLINE)
    if data:
        try:
            print("forward to host {}".format(conn))
            clientToServerDict[conn].send(data)
        except KeyError:
            print("forward to client {}".format(conn))
            serverToClientDict[conn].send(data)
    else:
        print("connection {} closed".format(conn))
        myselect.unregister(conn)
        conn.close()
        try:
            clientToServerDict[conn].close()
            del serverToClientDict[clientToServerDict[conn]]
            del  clientToServerDict[conn]
        except KeyError:
            serverToClientDict[conn].close()
            del clientToServerDict[serverToClientDict[conn]]
            del serverToClientDict[conn]
        

def createSocket(host, port):
    fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    fd.bind((host, port))
    fd.setblocking(False)
    fd.listen(5)
    myselect.register(fd, selectors.EVENT_READ, onAccept)
    return fd

def createConnection(host, port):
    fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    fd.connect(host, port)
    fd.setblocking(False)
    return fd

def main():

    
    for (localPort, hostPort) in config.PORT_HOSTS:
        fd = createSocket("", localPort)
        listenSocketForPort[fd] = hostPort
    while True:
        events = myselect.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)

if __name__ == '__main__':
    main()
