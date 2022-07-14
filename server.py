import socket
import hashlib
import os
import threading
import json
import tkinter as tk
import Crypto.Cipher.AES as AES
import Crypto.Cipher.PKCS1_OAEP as PKCS1_OAEP
from Crypto.PublicKey import RSA
from server_interface import ServerInterface
class Server():
    def __init__(self):
        self.data = {"quit": "False", "msg": {"sender": "", "text": ""}, "iv": ""}
        self.host = "127.0.0.1"
        self.port = 80
        self.clientsList = []
        self.status = "Offline"

        # Inicialização da interface do cliente
        self.myInterface()

    def startSocket(self, port):
        try:
            # Iniciando o socket
            self.port = int(port)
            self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serverSocket.bind((self.host, self.port))

        except BaseException as e:
            print(e)
            self.serverInterface.recvMsg("Falha: verifique endereço e porta utilizados.")

        else:            
            # Inicialização da thread de recebimento de clientes
            self.status = "Online"
            thread_recv = threading.Thread(target=self.newClients)
            thread_recv.start()
            self.serverInterface.recvMsg("Servidor rodando...")
    
    def newClients(self):
        while self.status == "Online":
            self.serverInterface.recvMsg("Esperando clientes...")
            try:
                # Servidor preparado para receber clientes
                self.serverSocket.listen(5)
                # Servidor cadastrando novo cliente
                socket_client, socket_client_address = self.serverSocket.accept()
                # Criando thread para o novo cliente
                new_client_thread = ClientThread(socket_client_address, socket_client, self)
                new_client_thread.start()
            except Exception as e:
                self.serverInterface.recvMsg(str(e))
                self.serverInterface.recvMsg("Falha no cadastro do novo cliente.")
            else:
                # Adicionando o novo cliente na lista de clientes
                self.clientsList.append(new_client_thread)
                self.serverInterface.recvMsg(f"Novo cliente conectado: {socket_client_address}")
        self.quit()

    # Método que chama a interface do servidor
    def myInterface(self):
        self.root = tk.Tk()
        self.serverInterface = ServerInterface(self, self.root)
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        self.root.mainloop()

    # Função para remover um cliente que desconectou
    def removeClient(self, client):
        self.clientsList.remove(client)
        self.serverInterface.recvMsg(f"Cliente {client.socketName} foi desconectado.")
    
    # Método para encerrar o servidor
    def quit(self):
        if len(self.clientsList):
            dataSend = self.data
            dataSend.update({"quit": "True"})
            dataEncoded = json.dumps(dataSend).encode()
            for clientThread in self.clientsList:
                clientThread.socketClient.sendall(dataEncoded)
                clientThread.socketClient.close()
            
        self.status = "Offline"
        self.root.destroy()

class ClientThread(threading.Thread):
    def __init__(self, socketClientAddress, socketClient, server):
        threading.Thread.__init__(self)
        self.server = server
        self.address = socketClientAddress
        self.socketClient = socketClient
        self.socketName = socketClient.getpeername()
        self.sessionKey = ""
        self.status = "Online"
        # Definição do formato dos dados de comunicação
        self.data = {"quit": "False", "msg": {"sender": "", "text": ""}, "iv": ""}

    def run(self):
        self.server.serverInterface.recvMsg("Aguardando chave pública do cliente...")
        
        # Recebendo chave pública do cliente
        strClientPubKey = self.socketClient.recv(2048)
        # Criando objeto de chave do cliente
        clientPubKey = RSA.importKey(strClientPubKey)
        clientCipher =  PKCS1_OAEP.new(clientPubKey)

        # Hashing da chave pública para validação
        hashObject = hashlib.sha1(strClientPubKey)
        publicKeyHash = hashObject.hexdigest()

        # Verificando se foi recebido uma chave não vazia
        if strClientPubKey != "":
            # Enviando confirmação
            self.socketClient.sendall("YES".encode())
            # Recebendo hash da chave pública do cliente
            publicKeyHashRecv = self.socketClient.recv(1024)
            publicKeyHashRecv = publicKeyHashRecv.decode()

        # Verificando se o hash calculado e o hash recebido conferem
        if publicKeyHash == publicKeyHashRecv:
            # Criando chave de sessão
            self.sessionKey = os.urandom(16)
            # Criptografando chave de sessão
            encryptSessionKey = clientCipher.encrypt(self.sessionKey)
            # Enviando chave de sessão criptografada para o cliente
            self.socketClient.sendall(encryptSessionKey)
            # HANDSHAKE COMPLETE

            # Iniciando a thread para recebimento de dados
            thread_recv = threading.Thread(target=self.recvData)
            thread_recv.start()
            thread_recv.join()
        else:
            self.server.serverInterface.recvMsg("Hash da chave pública não confere!")
        
        self.socketClient.close()        

    # Envia uma mensagem recebida no servidor para todos os clientes.
    def sendMessage(self, socketName, message):
        for clientThread in self.server.clientsList:
            # Criando o objeto de criptografia com a chave de sessão relativa a cada cliente
            aesCipherSession = AES.new(clientThread.sessionKey, AES.MODE_CFB)
            # Criptografando a mensagem
            msg = {"sender": str(socketName), "text": message}
            encryptedMsg = aesCipherSession.encrypt(json.dumps(msg).encode())

            # Montando pacote com os dados para enviar
            dataSend = self.data
            dataSend.update({"msg": encryptedMsg.decode("latin-1"), "iv": aesCipherSession.iv.decode("latin-1")})
            # Enviando dados para o cliente
            clientThread.socketClient.sendall(json.dumps(dataSend).encode())

    # Recebe dados dos clientes
    def recvData(self):
        while self.status == "Online":
            # Recebendo dados do cliente, e separando
            dataEncoded = self.socketClient.recv(1024)
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
                aesCipherSession = AES.new(self.sessionKey, AES.MODE_CFB,iv)
                decriptedMsg = json.loads(aesCipherSession.decrypt(msg).decode())
                
                # Reencaminha a mensagem
                self.sendMessage(decriptedMsg.get("sender", ""), decriptedMsg.get("text", ""))

if __name__ == "__main__":
    # Recebendo a porta que será utilizada pelo servidor
    # PORT = int(input("Port - > "))
    Server()
        