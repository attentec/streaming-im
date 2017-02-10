import message
import unittest

class MessageTests(unittest.TestCase):
    def test_encode_followed_by_decode(self):
        input_ = (123, 12345, b"hello world!") 
        msg = message.encode_message(*input_)
        output = message.decode_message(msg)
        self.assertEqual(output, input_)