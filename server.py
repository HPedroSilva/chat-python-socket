import socket
import hashlib
import os
import threading
import json
import Crypto.Cipher.AES as AES
import Crypto.Cipher.PKCS1_OAEP as PKCS1_OAEP
from Crypto.PublicKey import RSA

HOST = "127.0.0.1"
PORT = 80

class Server():
    def __init__(self):
        try:
            # Iniciando o socket
            server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            server.bind((HOST, PORT))
            print("Servidor rodando...")

        except BaseException:
            print ("Falha: verifique endereço e porta utilizados.")

        self.clientsList = []
        while True:
            print("Esperando clientes...")

            # Servidor preparado para receber clientes
            server.listen(5)

            # Servidor cadastrando novo cliente
            socket_client, socket_client_address = server.accept()
            # Criando thread para o novo cliente
            new_client_thread = ClientThread(socket_client_address, socket_client, self)
            new_client_thread.start()
            # Adicionando o novo cliente na lista de clientes
            self.clientsList.append(new_client_thread)
            print(f"Novo cliente conectado: {socket_client_address}")

    # Função para remover um cliente que desconectou
    def removeClient(self, client):
        self.clientsList.remove(client)
        print(f"Cliente {client.socketName} foi desconectado.")

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
        print ("Aguardando chave pública do cliente...")
        
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
            print ("Hash da chave pública não confere!")
        
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
            # Enviando dados para o clinte
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
        