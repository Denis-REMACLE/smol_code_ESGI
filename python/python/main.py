#!/usr/bin/env python3
import threading
import server
import client


def main():
    print("coucou")
    thread1 = threading.Thread(target=server.main)
    thread1.start()
    while True:
        thread2 = threading.Thread(target=client.main)
        thread2.start()
        thread2.join()

if __name__ == "__main__":
    main()