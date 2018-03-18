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
            host = clientToServerDict[conn]
            print("forward from client:{0}\nto host:{1}".format(conn, host))
            host.send(data)
        except KeyError:
            client = serverToClientDict[conn]
            print("forward from host:{0} to client:{1}".format(conn, client))
            client.send(data)
    else:
        print("connection {} closed".format(conn))
        myselect.unregister(conn)
        conn.close()
        try:
            server = clientToServerDict[conn]
            print("closing connection to server{}".format(server))
            server.close()
            del serverToClientDict[server]
            del  clientToServerDict[conn]
            myselect.unregister(server)
        except KeyError:
            client = serverToClientDict[conn]
            print("closing connection to client{}".format(client))
            client.close()
            del clientToServerDict[client]
            del serverToClientDict[conn]
            myselect.unregister(client)
        

def createSocket(host, port):
    fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    fd.bind((host, port))
    fd.setblocking(False)
    fd.listen(5)
    myselect.register(fd, selectors.EVENT_READ, onAccept)
    return fd

def createConnection(host, port):
    fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    fd.connect((host, port))
    #fd.setblocking(False)
    myselect.register(fd, selectors.EVENT_READ, onRead) 
    return fd

def main():

    
    for (hostPort, localPort) in config.LOCAL_SERVICE_PORTS.items():
        fd = createSocket("", localPort)
        listenSocketForPort[fd] = hostPort
    while True:
        events = myselect.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)

if __name__ == '__main__':
    main()
