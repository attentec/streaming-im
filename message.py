import struct

message_format = "!BH"

def encode_message(type_, seq, payload):
    return struct.pack(message_format, type_, seq) + payload

def decode_message(msg):
    header = msg[:3]
    payload = msg[3:]
    type_, seq = struct.unpack(message_format, header)
    return type_, seq, payload