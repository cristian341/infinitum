# encrypting
from cryptography.fernet import Fernet
message = "my deep dark secret".encode()

f = Fernet(key)
encrypted = f.encrypt(message)
print(encrypted)
# decrypting

f = Fernet(key)
decrypted = f.decrypt(encrypted)