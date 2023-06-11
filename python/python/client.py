#!/usr/bin/env python3
import socket

def main():
    booop = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    booop.connect(('127.0.0.1', 42069))
    response = booop.recv(512)
    print(response)
    booop.send(b"hi")

    response = booop.recv(512)
    print(response)
    booop.send(b"bye")
    booop.close()

if __name__ == "__main__":
    main()
