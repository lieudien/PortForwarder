import socket, select
import traceback

BUFSIZE = 1024
BACKLOG = 1024
EOL1 = b'\n\n'
EOL2 = b'\n\r\n'
response = 'Thank you for your message!'

def main(host, port):

    listenfd = createSocket(host, port)
    epoll = createEpoll()
    epoll.register(listenfd.fileno(), select.EPOLLIN | select.EPOLLET)

    try:
        conns = {}
        requests = {}
        responses = {}
        server_fd = listenfd.fileno()

        while True:
            events = epoll.poll(1)
            """print("Epoll wait...")"""
            for fileno, event in events:
                print("Event happend..")
                if fileno == server_fd:
                    acceptConn(listenfd, conns, requests, responses, epoll)
                elif event & select.EPOLLIN:
                    print("EPOLLIN")
                    receive_request(fileno, conns, requests, responses, epoll)
                elif event & select.EPOLLOUT:
                    print("EPOLLOUT")
                    send_response(fileno, conns, responses, epoll)
                elif event & select.EPOLLHUP:
                    print("EPOLLHUP")
                    epoll.unregister(fileno)
                    conns[fileno].close()
                    del conns[fileno]
    finally:
        epoll.unregister(listenfd.fileno())
        epoll.close()
        listenfd.close()

def createSocket(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        print("Listening for connection on port %d" % port)
        sock.setblocking(0)
        sock.listen(1)
        return sock
    except socket.error:
        print("create socket error")
        sock.close()

def createEpoll():
    try:
        epoll = select.epoll()
    except select.error:
        epoll.close()
    return epoll

def acceptConn(listenfd, conns, requests, responses, epoll):
    try:
        while True:
            conn, addr = listenfd.accept()
            print "Received connection from ", addr
            conn.setblocking(0)
            fd = conn.fileno()
            epoll.register(fd, select.EPOLLIN | select.EPOLLET)
            conns[fd] = conn
            requests[fd] = b''
            responses[fd] = response
    except socket.error:
        pass

def receive_request(fd, conns, requests, responses, epoll):
    try:
        while True:
            requests[fd] += conns[fd].recv(BUFSIZE)
    except Exception, e:
        pass
    """ Handle empty request """
    # if (requests[fd] == ''):
    #     print("[{:02d}] exit or hung up".format(fd))
    #     epoll.unregister(fd)
    #     conns[fd].close()
    #     del conns[fd], requests[fd], responses[fd]
    #     return
    # else:
    if EOL1 in requests[fd] or EOL2 in requests[fd]:
        epoll.modify(fd, select.EPOLLOUT | select.EPOLLET)
        print ('-'*40 + '\n' + requests [fd])

def send_response(fd, conns, responses, epoll):
    try:
        while len(responses[fd]) > 0:
            byteswritten = conns[fd].send(response)
            print("Sending message to {}".format(fd))
    except Exception, e:
        pass
    epoll.modify(fd, select.EPOLLET)
if __name__ == '__main__':
    try:
        main("", 7000)
    except KeyboardInterrupt as e:
        print("Server shutdown")
