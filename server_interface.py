import tkinter as tk
class ServerInterface():
    def __init__(self, server, master=None):
        self.server = server
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

        # Label porta
        self.portLabe = tk.Label(self.primeiroContainer, text="Porta onde o servidor estará disponível:", font=self.fontePadrao)
        self.portLabe.pack(side=tk.LEFT)

        # Campo de digitação da porta
        self.port = tk.Entry(self.primeiroContainer)
        self.port["width"] = 30
        self.port["font"] = self.fontePadrao
        self.port.pack(side=tk.LEFT)

        # Botão ok porta
        self.btnOkPort = tk.Button(self.primeiroContainer)
        self.btnOkPort["text"] = "Ok"
        self.btnOkPort["font"] = ("Calibri", "8")
        self.btnOkPort["width"] = 12
        self.btnOkPort["command"] = self.sendPort
        self.btnOkPort.pack()

        # Quadro que mostra as mensagens
        self.displayText = tk.Text(self.segundoContainer)
        self.displayText["width"] = 90
        self.displayText["font"] = self.fontePadrao
        self.displayText.pack(side=tk.LEFT)
        self.displayText.configure(state='disabled')

        # Botão encerrar servidor
        self.btnQuit = tk.Button(self.terceiroContainer)
        self.btnQuit["text"] = "Encerrar Servidor"
        self.btnQuit["font"] = ("Calibri", "8")
        self.btnQuit["width"] = 12
        self.btnQuit["command"] = self.server.quit
        self.btnQuit.pack()

        super().__init__()

    def recvMsg(self, msg):
        self.displayText.configure(state='normal')
        self.displayText.insert('end', f"{msg}\n")
        self.displayText.configure(state='disabled')

    def sendPort(self):
        if self.server.status == "Offline": 
            port = self.port.get()
            try:
                port = int(port)
                self.port.configure(state="disabled")
                self.server.startSocket(port)
            except:
                self.recvMsg("Insira um valor válido para a porta!")
        