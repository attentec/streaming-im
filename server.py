import itertools
import message
import socket
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = b"Hello, World!"

s = socket.socket(socket.AF_INET, # Internet
            socket.SOCK_DGRAM) # UDP

for i in itertools.count():
    message_type = 0
    msg = message.encode_message(message_type, i, MESSAGE)
    s.sendto(msg, (UDP_IP, UDP_PORT))
    time.sleep(1)
