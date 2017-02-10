import itertools
import message
import random
import socket
import time
import threading

LISTEN_ADDR = ("0.0.0.0", 5000)
MESSAGE = b"Hello, World!"

def debug(*args):
    print(*args)

def fetch_message(seq):
    return ("Hello #" + str(seq)).encode("utf-8")

def drop_message():
    return random.randrange(100) < 30

def wait_for_client(s):
    msg, addr = s.recvfrom(1024)
    debug("Start", addr)
    return addr

def send_to_client(s, addr):
    for i in itertools.count():
        msg = message.encode_message(message.MSG_TYPE, i, fetch_message(i))
        if not drop_message():
            debug("Send", i)
            s.sendto(msg, addr)
        else:
            debug("Drop", i)
        time.sleep(1)

def serve_retries(s):
    while True:
        in_msg, addr = s.recvfrom(1024)
        in_type, in_seq, in_payload = message.decode_message(in_msg)
        out_msg = message.encode_message(message.MSG_TYPE, in_seq, fetch_message(in_seq))
        if not drop_message():
            s.sendto(out_msg, addr)
            debug("Resend", in_seq)
        else:
            debug("Failed Resend", in_seq)

s = socket.socket(socket.AF_INET, # Internet
            socket.SOCK_DGRAM) # UDP
s.bind(LISTEN_ADDR)
addr = wait_for_client(s)
threading.Thread(target=lambda: serve_retries(s)).start()
send_to_client(s, addr)