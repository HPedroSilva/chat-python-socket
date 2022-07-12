import tkinter as tk
class Application(tk.Tk):
    def __init__(self, master=None):
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

        # self.titulo = Label(self.primeiroContainer, text="Dados do usuário")
        # self.titulo["font"] = ("Arial", "10", "bold")
        # self.titulo.pack()

        # self.nomeLabel = Label(self.segundoContainer,text="Nome", font=self.fontePadrao)
        # self.nomeLabel.pack(side=LEFT)

        # self.nome = Entry(self.segundoContainer)
        # self.nome["width"] = 30
        # self.nome["font"] = self.fontePadrao
        # self.nome.pack(side=LEFT)

        self.displayText = tk.Text(self.segundoContainer)
        self.displayText["width"] = 30
        self.displayText["font"] = self.fontePadrao
        self.displayText.pack(side=tk.LEFT)
        self.displayText.configure(state='disabled')

        self.senhaLabel = tk.Label(self.terceiroContainer, text="Mensagem", font=self.fontePadrao)
        self.senhaLabel.pack(side=tk.LEFT)

        self.msg = tk.Entry(self.terceiroContainer)
        self.msg["width"] = 30
        self.msg["font"] = self.fontePadrao
        # self.msg["show"] = "*"
        self.msg.pack(side=tk.LEFT)

        self.autenticar = tk.Button(self.quartoContainer)
        self.autenticar["text"] = "Enviar"
        self.autenticar["font"] = ("Calibri", "8")
        self.autenticar["width"] = 12
        self.autenticar["command"] = self.sendMsg
        self.autenticar.pack()

        self.mensagem = tk.Label(self.quartoContainer, text="", font=self.fontePadrao)
        self.mensagem.pack()
        super().__init__()

    def recvMsg(self, msg):
        self.displayText.configure(state='normal')
        self.displayText.insert('end', "\n" + str(msg))
        self.displayText.configure(state='disabled')

    def sendMsg(self):
        msg = self.msg.get()
        self.msg.delete(0, tk.END)
        print(msg)
    # #Método verificar senha
    # def verificaSenha(self):
    #     usuario = self.nome.get()
    #     senha = self.senha.get()
    #     if usuario == "usuariodevmedia" and senha == "dev":
    #         self.mensagem["text"] = "Autenticado"
    #     else:
    #         self.mensagem["text"] = "Erro na autenticação"

