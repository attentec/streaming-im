import message
import socket

SERVER_ADDR = ("127.0.0.1", 5000)

def debug(*args):
    pass

class MessageStore:
    def __init__(self):
        self.next_to_print = 0
        self.store = {}

    def iter_available(self):
        while self.next_to_print in self.store:
            msg = self.store.pop(self.next_to_print)
            yield msg
            self.next_to_print += 1
    
    def iter_to_request(self):
        if not self.store:
            return
        last_seen = sorted(self.store.keys())[-1]
        for seq in range(self.next_to_print, last_seen):
            if seq not in self.store:
                yield seq
    
    def store_message(self, msg):
        seq = msg[1]
        self.store[seq] = msg

def subscribe_to_server(s, addr):
    msg = message.encode_message(message.START_TYPE, 0, b"")
    debug("Start")
    s.sendto(msg, addr)

def request_message(s, addr, seq):
    msg = message.encode_message(message.REQ_TYPE, seq, b"")
    debug("Request", seq)
    s.sendto(msg, addr)

def receive_message(s):
    data, address = s.recvfrom(1024)
    return message.decode_message(data)
    
def receive_from_server(s, addr):
    msg_store = MessageStore()
    next_seq = 0
    store = {}

    while True:
        for msg in msg_store.iter_available():
            debug("Display", msg)
            payload = msg[2]
            print(payload)
        for seq in msg_store.iter_to_request():
            request_message(s, addr, seq)
        msg = receive_message(s)
        debug("Store", msg)
        msg_store.store_message(msg)

s = socket.socket(socket.AF_INET, # Internet
            socket.SOCK_DGRAM) # UDP
subscribe_to_server(s, SERVER_ADDR)
receive_from_server(s, SERVER_ADDR)