#Encrypts and decrypts
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

BS = 16

padding = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
remove_padding = lambda s : s[0:-s[-1]]

class AESCipher:

	def __init__( self, key ):
		self.key = hashlib.sha256(key.encode('utf-8')).digest()

	def encode_string(self, raw):
		raw = padding(raw)
		iv = Random.new().read( AES.block_size )
		cipher = AES.new( self.key, AES.MODE_CBC, iv )
		return base64.b64encode( iv + cipher.encrypt( raw ) )

	def decode_string(self, enc):
		enc = base64.b64decode(enc)
		iv = enc[:16]
		cipher = AES.new(self.key, AES.MODE_CBC, iv )
		return remove_padding(cipher.decrypt( enc[16:] ))