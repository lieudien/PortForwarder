#!/usr/bin/python3

import selectors
import socket

BUFLINE = 1024
myselect = selectors.DefaultSelector()

def onAccept(sock, mask):
    conn, addr = sock.accept()
    print("Received connect from {}".format(addr))
    conn.setblocking(False)
    myselect.register(conn, selectors.EVENT_READ, onRead)

def onRead(conn, mask):
    data = conn.recv(BUFLINE)
    if data:
        print("Send to client {}".format(conn))
        conn.send(data)
    else:
        print("Client {} closed".format(conn))
        myselect.unregister(conn)
        conn.close()

def createSocket(host, port):
    fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    fd.bind((host, port))
    fd.setblocking(False)
    fd.listen(5)
    myselect.register(fd, selectors.EVENT_READ, onAccept)

def main():

    fd = createSocket("", 7000)
    while True:
        events = myselect.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)

if __name__ == '__main__':
    main()
