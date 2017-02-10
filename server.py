import itertools
import message
import random
import socket
import time

UDP_IP = "127.0.0.1"
UDP_START_IP = "0.0.0.0"
UDP_PORT = 5005
UDP_START_PORT = 5006
MESSAGE = b"Hello, World!"


def drop_message():
    return random.randrange(100) < 10

def serve_client(host, port):
    s = socket.socket(socket.AF_INET, # Internet
                socket.SOCK_DGRAM) # UDP

    for i in itertools.count():
        message_type = 0
        msg = message.encode_message(message_type, i, MESSAGE)
        if not drop_message():
            s.sendto(msg, (host, port))
        time.sleep(1)

def wait_for_client():
    s = socket.socket(socket.AF_INET, # Internet
                socket.SOCK_DGRAM) # UDP
    s.bind((UDP_START_IP, UDP_START_PORT))
    msg, address = s.recvfrom(1024)
    return address

host, port = wait_for_client()    
serve_client(host, port)