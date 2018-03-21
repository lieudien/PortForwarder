#!/usr/bin/python3

import selectors
import socket
import config
import threading
from queue import Queue

#from multiprocessing import *

BUFLINE = 1024
listenSocketForPort = {}


class ForwardingThread(threading.Thread):

    def __init__(self, newFDQueue):

        threading.Thread.__init__(self)
        self._selector = selectors.EpollSelector()
        self._clientToServerDict = {}
        self._serverToClientDict = {}
        self._newFDQueue = newFDQueue
        threading.Thread(target=self.getQueuedSocket).start()

    
    def run(self):

        while True:
            events = self._selector.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)

    def onRead(self, conn, mask):
        data = conn.recv(BUFLINE)
        if data:
            try:
                host = self._clientToServerDict[conn]
                #print("forward from client:{0}\nto host:{1}".format(conn, host))
                host.send(data)
            except KeyError:
                client = self._serverToClientDict[conn]
                #print("forward from host:{0} to client:{1}".format(conn, client))
                client.send(data)
        else:
            print("connection {} closed".format(conn))
            self._selector.unregister(conn)
            conn.close()
            try:
                server = self._clientToServerDict[conn]
                print("closing connection to server{}".format(server))
                server.close()
                del self._serverToClientDict[server]
                del  self._clientToServerDict[conn]
                self._selector.unregister(server)
            except KeyError:
                client = self._serverToClientDict[conn]
                print("closing connection to client{}".format(client))
                client.close()
                del self._clientToServerDict[client]
                del self._serverToClientDict[conn]
                self._selector.unregister(client)


    def getQueuedSocket(self):
        while True:
            (fd, port) = self._newFDQueue.get()
            forwardFD = self.createConnection(config.PORT_HOSTS[port], port)
            self._clientToServerDict[fd] = forwardFD
            self._serverToClientDict[forwardFD] = fd
            self._selector.register(fd, selectors.EVENT_READ, self.onRead)
            self._selector.register(forwardFD, selectors.EVENT_READ, self.onRead)
            

    def createConnection(self, host, port):
        fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        fd.connect((host, port))
        fd.setblocking(False)
        return fd


class EpollPortForwarder(object):

    def __init__(self):

        self._selector = selectors.EpollSelector()
        self._socketNumber = 0
        self._socketQueues = []
        self._listenSocketForPort = {}

        for _ in range(config.WORKER_THREADS):
            socketQueue = Queue()
            self._socketQueues.append(socketQueue)
            proc = ForwardingThread(socketQueue)
            proc.start()

        for (hostPort, localPort) in config.LOCAL_SERVICE_PORTS.items():
            fd = self.createSocket("", localPort)
            self._listenSocketForPort[fd] = hostPort

        self.mainLoop()


    def onAccept(self, sock, mask):
        fd, addr = sock.accept()
        #print("Received connect from {}".format(addr))
        fd.setblocking(False)
        self._socketQueues[self._socketNumber % config.WORKER_THREADS].put((fd, self._listenSocketForPort[sock]))
        self._socketNumber += 1
        print('{0} connections'.format(self._socketNumber*2))


    def createSocket(self, host, port):
        fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        fd.bind((host, port))
        fd.setblocking(False)
        fd.listen(100)
        self._selector.register(fd, selectors.EVENT_READ, self.onAccept)
        return fd

    def mainLoop(self):

        while True:
            events = self._selector.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)

if __name__ == '__main__':
    forwarder = EpollPortForwarder()
    forwarder.mainLoop()
