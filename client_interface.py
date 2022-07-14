import tkinter as tk

# Interface principal do cliente
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

# Interface de formulário para porta e ip do servidor antes de abrir o cliente
class FormInterface():
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

        # Label ip do servidor
        self.ipLabel = tk.Label(self.primeiroContainer, text="IP do servidor:", font=self.fontePadrao)
        self.ipLabel.pack(side=tk.LEFT)

        # Campo de digitação de ip do servidor
        self.ip = tk.Entry(self.primeiroContainer)
        self.ip["width"] = 20
        self.ip["font"] = self.fontePadrao
        self.ip.pack(side=tk.LEFT)

        # Label porta do servidor
        self.portLabel = tk.Label(self.segundoContainer, text="Porta do servidor:", font=self.fontePadrao)
        self.portLabel.pack(side=tk.LEFT)

        # Campo de digitação da porta do servidor
        self.port = tk.Entry(self.segundoContainer)
        self.port["width"] = 20
        self.port["font"] = self.fontePadrao
        self.port.pack(side=tk.LEFT)

        # Botão ok
        self.btnOk = tk.Button(self.terceiroContainer)
        self.btnOk["text"] = "Ok"
        self.btnOk["font"] = ("Calibri", "8")
        self.btnOk["width"] = 12
        self.btnOk["command"] = self.send
        self.btnOk.pack()

        # Label de log
        self.logLabel = tk.Label(self.quartoContainer, text="", font=self.fontePadrao)
        self.logLabel.pack(side=tk.LEFT)

        super().__init__()

    # Método para enviar ip e porta inseridos para ser realizada a conexão
    def send(self):
        if self.client.status == "Offline": 
            ip = self.ip.get()
            port = self.port.get()
            try:
                port = int(port)
                self.ip.configure(state="disabled")
                self.port.configure(state="disabled")
                self.client.startSocket(ip, port)
            except:
                self.logLabel.config(text="Insira um valor válido para a porta!")
        