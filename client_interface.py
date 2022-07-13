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

        # Quadro que mostra as mensagens
        self.displayText = tk.Text(self.segundoContainer)
        self.displayText["width"] = 30
        self.displayText["font"] = self.fontePadrao
        self.displayText.pack(side=tk.LEFT)
        self.displayText.configure(state='disabled')

        self.msgLabel = tk.Label(self.terceiroContainer, text="Mensagem:", font=self.fontePadrao)
        self.msgLabel.pack(side=tk.LEFT)

        # Campo de digitação da mensagem
        self.msg = tk.Entry(self.terceiroContainer)
        self.msg["width"] = 30
        self.msg["font"] = self.fontePadrao
        self.msg.pack(side=tk.LEFT)

        # Botão enviar
        self.btnSend = tk.Button(self.quartoContainer)
        self.btnSend["text"] = "Enviar"
        self.btnSend["font"] = ("Calibri", "8")
        self.btnSend["width"] = 12
        self.btnSend["command"] = self.sendMsg
        self.btnSend.pack()

        super().__init__()

    def recvMsg(self, msg):
        self.displayText.configure(state='normal')
        self.displayText.insert('end', "\n" + str(msg))
        self.displayText.configure(state='disabled')

    def sendMsg(self):
        msg = self.msg.get()
        self.msg.delete(0, tk.END)
        self.client.send(msg)