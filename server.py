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

class ClientThread(threading.Thread):
    def __init__(self, clientId, socketClientAddress, socketClient):
        threading.Thread.__init__(self)
        self.id = clientId
        self.address = socketClientAddress
        self.socketClient = socketClient
        print ("Nova conexão criada com: ", self.address)
    
    def run(self):
        print ("CLIENT IS CONNECTED. CLIENT'S ADDRESS ->", self.address)
        print ("\n-----WAITING FOR PUBLIC KEY & PUBLIC KEY HASH-----\n")
        
        #client's message(Public Key)
        getpbk = self.socketClient.recv(2048)

        #conversion of string to KEY
        server_public_key = RSA.importKey(getpbk)
        key_cipher =  PKCS1_OAEP.new(server_public_key)

        #hashing the public key in server side for validating the hash from client
        hash_object = hashlib.sha1(getpbk)
        hex_digest = hash_object.hexdigest()

        if getpbk != "":
            print (getpbk)
            self.socketClient.sendall("YES".encode())
            gethash = self.socketClient.recv(1024)
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
            self.socketClient.sendall(E)
            while True:
                #message from client
                data_str = self.socketClient.recv(1024)
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
                    # client.sendall(eMsg)
                    eMsg = en.encrypt(mess.encode())
                    data = {"msg": eMsg.decode("latin-1"), "iv": en.iv.decode("latin-1")}
                    #converting the encrypted message to HEXADECIMAL to readable
                    #eMsg = eMsg.encode("hex").upper()
                    if eMsg:
                        print ("ENCRYPTED MESSAGE TO CLIENT-> "+str(eMsg))
                        print ("IV TO CLIENT-> "+str(en.iv))
                    self.socketClient.sendall(json.dumps(data).encode())
            self.socketClient.close()
        else:
            print ("\n-----PUBLIC KEY HASH DOESNOT MATCH-----\n")


#server address and port number input from admin
# host= input("Server Address - > ")
# port = int(input("Port - > "))
HOST = "127.0.0.1"
PORT = 80
#boolean for checking server and PORT
check = False
done = False

# def animate():
#     for c in itertools.cycle(['....','.......','..........','............']):
#         if done:
#             break
#         sys.stdout.write('\rCHECKING IP ADDRESS AND NOT USED PORT '+c)
#         sys.stdout.flush()
#         time.sleep(0.1)
#     sys.stdout.write('\r -----SERVER STARTED. WAITING FOR CLIENT-----\n')
try:
    #setting up socket
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((HOST,PORT))
    print("Servidor rodando...")
    check = True
except BaseException:
    print ("Falha: verifique endereço e porta utilizados.")
    check = False

if check is True: #Verificar
    # server Quit
    shutdown = False

cont = 0
while True:
    print("Esperando clientes...")
    server.listen(5)
    socket_client, socket_client_address = server.accept()
    new_thread = ClientThread(cont, socket_client_address, socket_client)
    new_thread.start()
    cont += 1