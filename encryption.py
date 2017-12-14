#Encrypts and decrypts
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

BS = 16

def padding(string):
	return string + " " * (AES.block_size - len(string) % AES.block_size)

class AESCipher:

	def __init__( self, key ):
		self.key = hashlib.sha256(key.encode('utf-8')).digest()

	def encode_string(self, raw):
		cipher = AES.new(self.key, AES.MODE_ECB)
		padded_data = padding(raw)
		enc = base64.b64encode(cipher.encrypt(padded_data))
		return enc

	def decode_string(self, enc):
		cipher = AES.new(self.key, AES.MODE_ECB)
		decoded_data = cipher.decrypt(base64.b64decode(enc))
		return decoded_data.strip()