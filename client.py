import message
import socket

UDP_IP = "0.0.0.0"
UDP_PORT = 5005

s = socket.socket(socket.AF_INET, # Internet
            socket.SOCK_DGRAM) # UDP
s.bind((UDP_IP, UDP_PORT))

while True:
    data, address = s.recvfrom(1024)
    type_, seq, payload = message.decode_message(data)
    print("header:", type_, seq)
    print("received message:", payload)
