#Encrypts and decrypts
import base64
from Crypto.Cipher import AES

def padding(string):
	sizeNeeded = AES.block_size - len(string) % AES.block_size
	for x in range(sizeNeeded):
		string += " "
	return string

def encode_string(key, string):
	string = padding(string)
	ba = bytearray()
	ba.extend(map(ord, string))
	length = 16 - (len(string) % 16)
	ba += bytes([length]) * length
	return base64.urlsafe_b64encode(ba)

def decode_string(key, string):
    string = base64.urlsafe_b64decode(string)
    string = string[:-string[-1]]
    return string.decode("utf-8").strip()