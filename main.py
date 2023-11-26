import base64
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto import Random
import cv2
import os

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

def get_private_key(password):
    salt = b"this is a salt"
    kdf = PBKDF2(password, salt, 64, 1000)
    key = kdf[:32]
    return key

def encrypt(raw, password):
    private_key = get_private_key(password)
    raw = pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    encrypted_text = iv + cipher.encrypt(raw.encode("utf-8"))
    return base64.b64encode(encrypted_text)
 
def decrypt(enc, password):
    private_key = get_private_key(password)
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    decrypted_bytes = unpad(cipher.decrypt(enc[16:]))
    decrypted_string = decrypted_bytes.decode("utf-8")
    return decrypted_string

''' Reading and Encryption stage '''

img=cv2.imread(input("enter image file directory : "))
msg=input("enter the secret msg : ")
password = input("Enter encryption password: ")
encryptedAES = encrypt(msg, password).decode("utf-8")

print(encryptedAES)

d={}
c={}
for i in range(255):
   d[chr(i)]=i
   c[i]=chr(i)
   
m=0
n=0
z=0

for i in range(len(encryptedAES)):
    img[n,m,z]=d[encryptedAES[i]]
    n+=1
    m+=1
    z=(z+1)%3
    
cv2.imwrite("encryptedimage.jpg",img)
os.startfile("encryptedimage.jpg")

'''Decryption Stage'''

retriveimgAES=""

pas=input("enter the decrypting password: ")

m=0
n=0
z=0

if(password==pas):
    for i in range(len(encryptedAES)):
        retriveimgAES =retriveimgAES+c[img[n,m,z]]
        n+=1
        m+=1
        z=(z+1)%3
    print("Decrypted message is : ",decrypt(retriveimgAES, password))
else:
    print("invalid password")
