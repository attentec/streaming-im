import message
import socket

UDP_IP = "0.0.0.0"
UDP_START_IP = "127.0.0.1"
UDP_PORT = 5005
UDP_START_PORT = 5006

def subscribe_to_server(host, port):
    s = socket.socket(socket.AF_INET, # Internet
                socket.SOCK_DGRAM) # UDP
    s.bind((UDP_IP, UDP_PORT))
    s.sendto(b"", (host, port))

def receive_from_server(host, port):
    s = socket.socket(socket.AF_INET, # Internet
                socket.SOCK_DGRAM) # UDP
    s.bind((host, port))

    while True:
        data, address = s.recvfrom(1024)
        type_, seq, payload = message.decode_message(data)
        print("header:", type_, seq)
        print("received message:", payload)

subscribe_to_server(UDP_START_IP, UDP_START_PORT)
receive_from_server(UDP_IP, UDP_PORT)