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
        
