#!/usr/bin/python

import socket, threading, logging, sys, time

BUFLINE = 1024
CLIENT_COUNTS = 10
logging.basicConfig(format='%(asctime)s %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p',
                filename='client_output.log',
                filemode='w',
                level=logging.DEBUG)

def write_message(message=None):
    logging.debug(message)
    print("%s\n" % message)

def client_task(host, port, i):
    fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("host={} port={}".format(host, port))
    fd.connect((host, port))
    try:
        while True:
            msg = "Hello message from {}".format(i)
            fd.send(msg)
            data = fd.recv(BUFLINE)
            print("Received from Server:", data)
            time.sleep(1)
    except KeyboardInterrupt:
        print("socket {} closed".format(i))
        fd.close()

def main():
    if len(sys.argv) == 3:
        serverHost = sys.argv[1]
        serverPort = int(sys.argv[2])
    else:
        print("Usage: ./client.py [host] [port]\n")
        return
    threads = []
    for i in range(CLIENT_COUNTS):
        thread = threading.Thread(target=client_task, args=(serverHost, serverPort, i, ))
        thread.daemon = True
        threads.append(thread)

    # for i in range(CLIENT_COUNTS):
    #     threads[i].start()
    #     threads[i].join()

if __name__ == '__main__':
    main()

