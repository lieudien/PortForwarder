#!/usr/bin/python

import socket, threading, logging, sys, time
import multiprocessing

BUFLINE = 1024
CLIENT_COUNTS = 4000

logging.basicConfig(format='%(asctime)s %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p',
                filename='client_output.log',
                filemode='w',
                level=logging.DEBUG)

def write_message(message=None):
    logging.debug(message)
    print("%s\n" % message)

def thread_task(host, port, i):
    fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    fd.connect((host, port))
    print("Thread {} is running...\n".format(i))
    try:
        while True:
            msg = b"Hello message"
            fd.send(msg)
            data = fd.recv(BUFLINE)
            print("Thread {} received from the server...\n".format(i))
            time.sleep(1)
    except socket.error:
        print("Disconnected from server. Thread {} stopped\n".format(i))
    finally:
        fd.close()

def process_task(host, port):
    threads = []
    for i in range(CLIENT_COUNTS):
        thread = threading.Thread(target=thread_task, args=(host, port, i, ))
        thread.daemon = True
        threads.append(thread)
        thread.start()
        time.sleep(0.02)

    for i in range(CLIENT_COUNTS):
        threads[i].join()

def main():
    if len(sys.argv) == 3:
        serverHost = sys.argv[1]
        serverPort = int(sys.argv[2])
    else:
        print("Usage: ./client.py [host] [port]\n")
        return

    pool = []
    for i in range(multiprocessing.cpu_count()):
        #thread = threading.Thread(target=thread_task, args=(serverHost, serverPort, i, ))
        #thread.start()
        proc = multiprocessing.Process(target=process_task, args=(serverHost, serverPort, ))
        pool.append(proc)
        proc.start()
        proc.join()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Client stopped")
