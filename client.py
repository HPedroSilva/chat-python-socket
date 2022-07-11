import time
import socket
import threading
import hashlib
import itertools
import json
import sys
from Crypto import Random
import Crypto.Cipher.AES as AES
import Crypto.Cipher.PKCS1_OAEP as PKCS1_OAEP
from Crypto.PublicKey import RSA

#animating loading
done = False
def animate():
    for c in itertools.cycle(['....','.......','..........','............']):
        if done:
            break
        sys.stdout.write('\rCONFIRMING CONNECTION TO SERVER '+c)
        sys.stdout.flush()
        time.sleep(0.1)

#public key and private key
random_generator = Random.new().read
key = RSA.generate(1024,random_generator)
public = key.publickey().exportKey()
private = key.exportKey()
key_cipher =  PKCS1_OAEP.new(key)

#hashing the public key
hash_object = hashlib.sha1(public)
hex_digest = hash_object.hexdigest()

#Setting up socket
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#host and port input user
#host = input("Server Address To Be Connected -> ")
#port = int(input("Port of The Server -> "))
host = "127.0.0.1"
port = 80
#binding the address and port
server.connect((host, port))
# printing "Server Started Message"
thread_load = threading.Thread(target=animate)
thread_load.start()

time.sleep(4)
done = True

def send(t,name,key):
    mess = input(name + " : ")
    #key = key[:16]
    #merging the message and the name
    whole = name+" : "+mess
    en_send = AES.new(key,AES.MODE_CFB)
    eMsg = en_send.encrypt(whole.encode())
    data = {"msg": eMsg.decode("latin-1"), "iv": en_send.iv.decode("latin-1")}
    #converting the encrypted message to HEXADECIMAL to readable
    #eMsg = eMsg.encode("hex").upper()
    if eMsg:
        print ("ENCRYPTED MESSAGE TO SERVER-> "+str(eMsg))
        print ("IV TO SERVER-> "+str(en_send.iv))
    server.send(json.dumps(data).encode())
    
def recv(t,key):
    data_str = server.recv(1024)
    data = json.loads(data_str.decode())
    newmess = data["msg"].encode("latin-1")
    iv = data["iv"].encode("latin-1")

    print ("\nENCRYPTED MESSAGE FROM SERVER-> " + str(newmess))
    print ("\nIV FROM SERVER -> "+str(iv))
    #key = key[:16]
    #decoded = newmess.decode("hex")
    en_recv = AES.new(key,AES.MODE_CFB,iv)
    dMsg = en_recv.decrypt(newmess)
    print ("\n**New Message From Server**  " + time.ctime(time.time()) + " : " + str(dMsg) + "\n")

while True:
    server.send(public)
    confirm = server.recv(1024)
    confirm = confirm.decode()
    if confirm == "YES":
        print(f"Confirmação do servidor: {hex_digest}")
        server.send(hex_digest.encode())
    else:
        break

    #connected msg
    msg = server.recv(1024)
    en = msg
    
    decrypt = key_cipher.decrypt(en)
    # hashing sha1
    en_object = hashlib.sha1(decrypt)
    en_digest = en_object.hexdigest()

    print ("\n-----ENCRYPTED PUBLIC KEY AND SESSION KEY FROM SERVER-----")
    print (msg)
    print ("\n-----DECRYPTED SESSION KEY-----")
    print (decrypt)
    print ("\n-----HANDSHAKE COMPLETE-----\n")
    alais = input("\nYour Name -> ")

    while True:
            
        thread_send = threading.Thread(target=send,args=("------Sending Message------",alais,decrypt))
        thread_recv = threading.Thread(target=recv,args=("------Recieving Message------",decrypt))
        thread_send.start()
        thread_recv.start()

        thread_send.join()
        thread_recv.join()
        time.sleep(0.5)
    time.sleep(60)
    server.close()
server.close()