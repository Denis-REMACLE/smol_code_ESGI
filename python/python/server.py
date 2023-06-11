#!/usr/bin/env python3
import socket
import threading

def manage_client(booop):
    booop.send(b"hello")
    response = booop.recv(512)
    print(response)
    booop.send(b"bye")
    response = booop.recv(512)
    print(response)
    booop.close

def main():
    biiip = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    biiip.bind(('127.0.0.1', 42069))
    biiip.listen(5)
    while True:
        (booop, address) = biiip.accept()
        bipbop = threading.Thread(target=manage_client, args=(booop, ))
        bipbop.run()

if __name__ == "__main__":
    main()