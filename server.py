import socket
import hashlib
import os
import time
import itertools
import threading
import sys
import json
import Crypto.Cipher.AES as AES
import Crypto.Cipher.PKCS1_OAEP as PKCS1_OAEP
from Crypto.PublicKey import RSA

#server address and port number input from admin
# host= input("Server Address - > ")
# port = int(input("Port - > "))
host = "127.0.0.1"
port = 80
#boolean for checking server and port
check = False
done = False

def animate():
    for c in itertools.cycle(['....','.......','..........','............']):
        if done:
            break
        sys.stdout.write('\rCHECKING IP ADDRESS AND NOT USED PORT '+c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r -----SERVER STARTED. WAITING FOR CLIENT-----\n')
try:
    #setting up socket
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((host,port))
    server.listen(5)
    check = True
except BaseException:
    print ("-----Check Server Address or Port-----")
    check = False

if check is True:
    # server Quit
    shutdown = False
# printing "Server Started Message"
thread_load = threading.Thread(target=animate)
thread_load.start()

time.sleep(4)
done = True
#binding client and address
client,address = server.accept()
print ("CLIENT IS CONNECTED. CLIENT'S ADDRESS ->",address)
print ("\n-----WAITING FOR PUBLIC KEY & PUBLIC KEY HASH-----\n")

#client's message(Public Key)
getpbk = client.recv(2048)

#conversion of string to KEY
server_public_key = RSA.importKey(getpbk)
key_cipher =  PKCS1_OAEP.new(server_public_key)

#hashing the public key in server side for validating the hash from client
hash_object = hashlib.sha1(getpbk)
hex_digest = hash_object.hexdigest()

if getpbk != "":
    print (getpbk)
    client.send("YES".encode())
    gethash = client.recv(1024)
    gethash = gethash.decode()
    print ("\n-----HASH OF PUBLIC KEY----- \n"+gethash)
if hex_digest == gethash:
    # creating session key
    key_128 = os.urandom(16)
    #encrypt CTR MODE session key
    en = AES.new(key_128,AES.MODE_CFB)
    encrypto = en.encrypt(key_128)
    #hashing sha1
    en_object = hashlib.sha1(encrypto)
    en_digest = en_object.hexdigest()

    print ("\n-----SESSION KEY-----\n"+str(key_128))

    #encrypting session key and public key
    E = key_cipher.encrypt(key_128)
    print ("\n-----ENCRYPTED PUBLIC KEY AND SESSION KEY-----\n"+str(E))
    
    print ("\n-----HANDSHAKE COMPLETE-----")
    client.send(E)
    while True:
        #message from client
        data_str = client.recv(1024)
        data = json.loads(data_str.decode())
        newmess = data["msg"].encode("latin-1")
        iv = data["iv"].encode("latin-1")
        #decoding the message from HEXADECIMAL to decrypt the ecrypted version of the message only
        #decoded = newmess.decode("hex")
        #making en_digest(session_key) as the key
        key = en_digest[:16]
        print ("\nENCRYPTED MESSAGE FROM CLIENT -> "+str(newmess))
        print ("\nIV FROM CLIENT -> "+str(iv))
        #decrypting message from the client
        en = AES.new(key_128,AES.MODE_CFB,iv)
        dMsg = en.decrypt(newmess)
        print ("\n**New Message**  "+time.ctime(time.time()) +" > "+str(dMsg)+"\n")
        mess = input("\nMessage To Client -> ")
        if mess != "":
            #eMsg = eMsg.encode("hex").upper()
            en = AES.new(key_128,AES.MODE_CFB)
            # eMsg = en.encrypt(mess.encode())
            # if eMsg != "":
            #     print ("ENCRYPTED MESSAGE TO CLIENT-> " + str(eMsg))
            # client.send(eMsg)
            eMsg = en.encrypt(mess.encode())
            data = {"msg": eMsg.decode("latin-1"), "iv": en.iv.decode("latin-1")}
            #converting the encrypted message to HEXADECIMAL to readable
            #eMsg = eMsg.encode("hex").upper()
            if eMsg:
                print ("ENCRYPTED MESSAGE TO CLIENT-> "+str(eMsg))
                print ("IV TO CLIENT-> "+str(en.iv))
            client.send(json.dumps(data).encode())
    client.close()
else:
    print ("\n-----PUBLIC KEY HASH DOESNOT MATCH-----\n")