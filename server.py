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
    def __init__(self, socketClientAddress, socketClient):
        threading.Thread.__init__(self)
        self.address = socketClientAddress
        self.socketClient = socketClient
        self.key_128 = ""
        print ("Nova conexão criada com: ", self.address)
    



    def sendMessage(self, message):
        for clientThread in clientsList:
            en = AES.new(clientThread.key_128,AES.MODE_CFB)
            eMsg = en.encrypt(message)
            data = {"msg": eMsg.decode("latin-1"), "iv": en.iv.decode("latin-1")}
            if eMsg:
                print ("ENCRYPTED MESSAGE TO CLIENT-> "+str(eMsg))
                print ("IV TO CLIENT-> "+str(en.iv))
            clientThread.socketClient.sendall(json.dumps(data).encode())

    def recvData(self, socketClient, en_digest, key_128):
        while True:
            #message from client
            data_str = socketClient.recv(1024)
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
            self.sendMessage(dMsg)

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
            self.key_128 = os.urandom(16)
            #encrypt CTR MODE session key
            en = AES.new(self.key_128,AES.MODE_CFB)
            encrypto = en.encrypt(self.key_128)
            #hashing sha1
            en_object = hashlib.sha1(encrypto)
            en_digest = en_object.hexdigest()

            print ("\n-----SESSION KEY-----\n"+str(self.key_128))

            #encrypting session key and public key
            E = key_cipher.encrypt(self.key_128)
            print ("\n-----ENCRYPTED PUBLIC KEY AND SESSION KEY-----\n"+str(E))
            print ("\n-----HANDSHAKE COMPLETE-----")
            self.socketClient.sendall(E)
            while True:
                #thread_send = threading.Thread(target=sendData,args=(self. socketClient, self.key_128))
                print("aqui")
                thread_recv = threading.Thread(target=self.recvData,args=(self.socketClient, en_digest, self.key_128))
                #thread_send.start()
                thread_recv.start()
                #thread_send.join()
                thread_recv.join()
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

clientsList = []
while True:
    print("Esperando clientes...")
    server.listen(5)
    socket_client, socket_client_address = server.accept()
    new_client_thread = ClientThread(socket_client_address, socket_client)
    new_client_thread.start()
    clientsList.append(new_client_thread)