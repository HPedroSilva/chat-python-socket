import socket
import threading
import hashlib
import json
import tkinter as tk
from Crypto import Random
import Crypto.Cipher.AES as AES
import Crypto.Cipher.PKCS1_OAEP as PKCS1_OAEP
from Crypto.PublicKey import RSA
from client_interface import Interface, FormInterface

class Client:
    def __init__(self):
        self.status = "Offline"
        # Definição do formato dos dados de comunicação
        self.data = {"quit": "False", "msg": {"sender": "", "text": ""}, "iv": ""}
        self.host = "127.0.0.1"
        self.port = 80

        # Geração das chaves RSA
        random_generator = Random.new().read
        self.rsaKey = RSA.generate(1024, random_generator)
        self.publicKey = self.rsaKey.publickey().exportKey()
        privateKey = self.rsaKey.exportKey()

        # Hashing da chave pública
        hashObject = hashlib.sha1(self.publicKey)
        self.publicKeyHash = hashObject.hexdigest()
        self.myFormInterface()
        
    def startSocket(self, ip, port):
        self.host = ip
        self.port = port
        try:
            # Iniciando o Socket
            self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.server.connect((self.host, self.port))
        
        except Exception as e:
            print(e)
            print("Erro na criação do socket. Verifique endereço e porta utilizados!")
        
        else:
            self.status = "Online"
            # Cliente envia sua chave pública ao servidor para iniciar comunicação
            self.server.sendall(self.publicKey)
            # Servidor envia confirmação
            confirm = self.server.recv(1024).decode()
            if confirm == "YES":
                # Cliente envia hash da chave pública para confirmação do servidor
                self.server.sendall(self.publicKeyHash.encode())

                # Servidor envia chave de sessão criptografada
                encryptedSessionKey = self.server.recv(1024)

                # Descriptografando chave de sessão utilizando chave RSA
                publicKeyCipher =  PKCS1_OAEP.new(self.rsaKey)
                self.decryptedSessionKey = publicKeyCipher.decrypt(encryptedSessionKey)

                # Inicialização da thread de recebimento de mensagens no cliente
                thread_recv = threading.Thread(target=self.recv)
                thread_recv.start()

                # Inicialização da interface do cliente
                self.rootForm.destroy()
                self.myInterface()
                thread_recv.join()
            
            self.status = "Offline"
            self.server.close()

    # Método que chama a interface de inserir ip e porta do servidor
    def myFormInterface(self):
        self.rootForm = tk.Tk()
        self.clientFormInterface = FormInterface(self, self.rootForm)
        self.rootForm.mainloop()

    # Método que chama a interface principal do cliente
    def myInterface(self):
        self.root = tk.Tk()
        self.clientInterface = Interface(self, self.root)
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        self.root.bind('<Return>', self.clientInterface.sendMsgEnter)
        self.root.mainloop()

    # Método para fechar a conexão
    def quit(self):
        dataSend = self.data
        dataSend.update({"quit": "True"})
        dataEncoded = json.dumps(dataSend).encode()
        self.status = "Offline"
        self.server.sendall(dataEncoded)
        self.root.destroy()
        self.server.close()
    
    # Método para enviar mensagens para o servidor
    def send(self, sender, message):
        senderName = sender if sender else self.server.getsockname()
        # Criptografando a mensagem com a chave de sessão
        aesCipher = AES.new(self.decryptedSessionKey,AES.MODE_CFB)
        msg = {"sender": senderName, "text": message}
        encryptedMsg = aesCipher.encrypt(json.dumps(msg).encode())
        
        # Montando pacote com os dados para enviar
        dataSend = self.data
        dataSend.update({"msg": encryptedMsg.decode("latin-1"), "iv": aesCipher.iv.decode("latin-1")})
        dataEncoded = json.dumps(dataSend).encode()
        
        # Enviando dados para o servidor
        self.server.sendall(dataEncoded)

    # Método para receber mensagens do servidor
    def recv(self):
        while self.status == "Online":
            # Recebendo os dados do servidor, e separando
            try:
                dataEncoded = self.server.recv(1024)
                data = json.loads(dataEncoded.decode())
                quit = data.get("quit", "")
                msg = data.get("msg", "").encode("latin-1")
                iv = data.get("iv", "").encode("latin-1")

                if quit == "True":
                    self.socketClient.close()
                    self.status = "Offline"
                    self.server.removeClient(self)
                else:
                    # Descriptografando mensagem recebida
                    aesCipherSession = AES.new(self.decryptedSessionKey, AES.MODE_CFB, iv)
                    decriptedMsg = json.loads(aesCipherSession.decrypt(msg).decode())
                    
                    # Enviando mensagem para a interface
                    self.clientInterface.recvMsg(decriptedMsg.get("sender", ""), decriptedMsg.get("text", ""))
            except:
                print("Erro ao receber dados do servidor.")
                break

if __name__ == "__main__":
    Client()