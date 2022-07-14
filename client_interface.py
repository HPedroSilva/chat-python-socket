import tkinter as tk
class Interface():
    def __init__(self, client, master=None):
        self.client = client
        self.fontePadrao = ("Arial", "10")

        self.primeiroContainer = tk.Frame(master)
        self.primeiroContainer["pady"] = 10
        self.primeiroContainer.pack()

        self.segundoContainer = tk.Frame(master)
        self.segundoContainer["padx"] = 20
        self.segundoContainer.pack()

        self.terceiroContainer = tk.Frame(master)
        self.terceiroContainer["padx"] = 20
        self.terceiroContainer.pack()

        self.quartoContainer = tk.Frame(master)
        self.quartoContainer["pady"] = 20
        self.quartoContainer.pack()

        # Label do nome
        self.nomeLabel = tk.Label(self.primeiroContainer, text="Seu nome:", font=self.fontePadrao)
        self.nomeLabel.pack(side=tk.LEFT)

        # Campo de digitação de nome
        self.nome = tk.Entry(self.primeiroContainer)
        self.nome["width"] = 30
        self.nome["font"] = self.fontePadrao
        self.nome.pack(side=tk.LEFT)

        # Quadro que mostra as mensagens
        self.displayText = tk.Text(self.segundoContainer)
        self.displayText["width"] = 90
        self.displayText["font"] = self.fontePadrao
        self.displayText.pack(side=tk.LEFT)
        self.displayText.configure(state='disabled')

        self.msgLabel = tk.Label(self.quartoContainer, text="Mensagem:", font=self.fontePadrao)
        self.msgLabel.pack(side=tk.LEFT)

        # Campo de digitação da mensagem
        self.msg = tk.Entry(self.quartoContainer)
        self.msg["width"] = 70
        self.msg["font"] = self.fontePadrao
        self.msg.pack(side=tk.LEFT)

        # Botão enviar
        self.btnSend = tk.Button(self.quartoContainer)
        self.btnSend["text"] = "Enviar"
        self.btnSend["font"] = ("Calibri", "8")
        self.btnSend["width"] = 12
        self.btnSend["command"] = self.sendMsg
        self.btnSend.pack()

        self.btnQuit = tk.Button(self.primeiroContainer)
        self.btnQuit["text"] = "Sair"
        self.btnQuit["font"] = ("Calibri", "8")
        self.btnQuit["width"] = 12
        self.btnQuit["command"] = self.client.quit
        self.btnQuit.pack()

        super().__init__()

    def recvMsg(self, sender, msg):
        self.displayText.configure(state='normal')
        self.displayText.insert('end', f"\n{str(sender)}: {str(msg)}")
        self.displayText.configure(state='disabled')

    def sendMsgEnter(self, event):
        self.sendMsg()

    def sendMsg(self):
        msg = self.msg.get()
        nome = self.nome.get()
        self.msg.delete(0, tk.END)
        self.client.send(nome, msg)
        