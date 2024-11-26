import tkinter as tk
from tkinter import ttk, messagebox
from validate_docbr import CPF
from banco import Banco
from conta import Conta
from pessoa import Pessoa
from titular import Titular
from conta_corrente import ContaCorrente
from conta_poupanca import ContaPoupanca
from gerencia_banco_dados import gerencia_banco_dados

class BancoApp:
    def __init__(self, banco):
        self.banco = banco
        self.root = tk.Tk()
        self.root.geometry("500x400")
        self.root.title("Sistema Bancário")
        self.root.configure(bg="#34495e")
        self.__cpf = None  # Definindo o atributo __cpf

        # Tema e estilo
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#ecf0f1", font=("Helvetica", 12))
        style.configure("TButton", background="#3498db", font=("Helvetica", 10, "bold"), padding=10)
        style.map("TButton", background=[("active", "#2980b9")])

        # Tela de login
        self.tela_login()

    def tela_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg="#ecf0f1", padx=20, pady=20)
        frame.pack(expand=True)

        ttk.Label(frame, text="Login:", font=("Helvetica", 12)).grid(row=0, column=0, sticky="w")
        self.login_entry = ttk.Entry(frame, font=("Helvetica", 12))
        self.login_entry.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="Senha:", font=("Helvetica", 12)).grid(row=1, column=0, sticky="w")
        self.senha_entry = ttk.Entry(frame, show="*", font=("Helvetica", 12))
        self.senha_entry.grid(row=1, column=1, pady=5)

        ttk.Button(frame, text="Entrar", command=self.verificar_login).grid(row=2, columnspan=2, pady=10)
        ttk.Button(frame, text="Criar Conta", command=self.tela_criar_conta).grid(row=3, columnspan=2, pady=5)

    def verificar_login(self):
        login = self.login_entry.get().strip()
        senha = self.senha_entry.get().strip()
        
        print(f"DEBUG: Login fornecido: {login}")  # Verificar o login fornecido
        print(f"DEBUG: Senha fornecida: {senha}")  # Verificar a senha fornecida

        # Verifique se login ou senha estão vazios
        if not login or not senha:
            messagebox.showerror("Erro", "Login ou senha não podem estar vazios.")
            return

        conta = self.banco.procurar_conta_por_login(login)  # Procura a conta pelo login

        if conta:
            # Verifica se a senha fornecida não é None ou vazia
            if senha:  # Verifica se a senha fornecida não está vazia
                senha_hash = Titular.hash_senha(senha)  # Gera o hash da senha fornecida

                if senha_hash == conta.titular.get_senha():  # Verifica se o hash da senha bate com o armazenado
                    messagebox.showinfo("Sucesso", f"Bem-vindo(a), {conta.titular.nome}!")
                    self.tela_principal(conta)
                else:
                    messagebox.showerror("Erro", "Senha incorreta.")
            else:
                messagebox.showerror("Erro", "Senha não fornecida.")
        else:
            messagebox.showerror("Erro", "Login não encontrado.")

    def tela_criar_conta(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg="#ecf0f1", padx=20, pady=20)
        frame.pack(expand=True)

        ttk.Label(frame, text="Nome:").grid(row=0, column=0, sticky="w")
        self.nome_entry = ttk.Entry(frame)
        self.nome_entry.grid(row=0, column=1)

        ttk.Label(frame, text="Idade:").grid(row=1, column=0, sticky="w")
        self.idade_entry = ttk.Entry(frame)
        self.idade_entry.grid(row=1, column=1)

        ttk.Label(frame, text="CPF:").grid(row=2, column=0, sticky="w")
        self.cpf_entry = ttk.Entry(frame)
        self.cpf_entry.grid(row=2, column=1)

        ttk.Label(frame, text="Login:").grid(row=3, column=0, sticky="w")
        self.novo_login_entry = ttk.Entry(frame)
        self.novo_login_entry.grid(row=3, column=1)

        ttk.Label(frame, text="Senha:").grid(row=4, column=0, sticky="w")
        self.nova_senha_entry = ttk.Entry(frame, show="*")
        self.nova_senha_entry.grid(row=4, column=1)

        ttk.Label(frame, text="Tipo de Conta:").grid(row=5, column=0, sticky="w")
        self.tipo_conta_entry = ttk.Entry(frame)
        self.tipo_conta_entry.grid(row=5, column=1)

        ttk.Button(frame, text="Criar", command=self.criar_conta).grid(row=6, columnspan=2, pady=10)
        ttk.Button(frame, text="Voltar", command=self.tela_login).grid(row=7, columnspan=2, pady=5)

    def criar_conta(self):
        nome = self.nome_entry.get().strip()
        idade = self.idade_entry.get().strip()
        cpf = self.cpf_entry.get().strip()
        login = self.novo_login_entry.get().strip()
        senha = self.nova_senha_entry.get().strip()
        tipo = self.tipo_conta_entry.get().strip()

        # Mensagem de depuração 
        print(f"DEBUG: nome={nome}, idade={idade}, cpf={cpf}, login={login}, senha={senha}, tipo={tipo}")

        if not nome.isalpha():
            messagebox.showerror("Erro", "O nome deve conter apenas letras.")
            return

        if not (18 <= int(idade) <= 100):
            messagebox.showerror("Erro", "Idade deve ser um número válido. Entre 18 e 100.")
            return

        if not login:
            messagebox.showerror("Erro", "Login não pode ser vazio.")
            return
        
        # Valida a senha antes de prosseguir
        if not Titular.validar_senha(senha):
            messagebox.showerror("Erro", "A senha não atende aos requisitos de segurança.")
            return

        validador_cpf = CPF()
        if not validador_cpf.validate(cpf):
            messagebox.showerror("Erro", "CPF inválido.")
            return
            
        if tipo != "ContaCorrente" and tipo != "ContaPoupanca":
            messagebox.showerror("Erro", "Tipo de conta deve ser ContaCorrente ou ContaPoupanca.")
            return

        try:
            mensagem = banco.adicionar_conta(nome, idade, cpf, login, senha, tipo)
            messagebox.showinfo("Info", mensagem)
            if mensagem == "Conta criada com sucesso!":
                self.tela_login()
        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    def tela_principal(self, conta):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg="#ecf0f1", padx=20, pady=20)
        frame.pack(expand=True)

        ttk.Label(frame, text=f"Bem-vindo(a), {conta.titular.nome}!", font=("Helvetica", 14)).pack(pady=10)
        ttk.Label(frame, text=f"Saldo: R$ {conta.saldo}").pack(pady=5)

        ttk.Button(frame, text="Depositar", command=lambda: self.tela_depositar(conta)).pack(pady=5)
        ttk.Button(frame, text="Sacar", command=lambda: self.tela_sacar(conta)).pack(pady=5)
        ttk.Button(frame, text="Transferir", command=lambda: self.tela_transferir(conta)).pack(pady=5)
        ttk.Button(frame, text="Histórico", command=lambda: self.tela_historico(conta)).pack(pady=5)

    def iniciar(self):
        self.root.mainloop()

try:
    gerenciador_db = gerencia_banco_dados(host='localhost',
                user='usuario_trabalho',
                password='senha_segura',
                database='banco_trabalho')
    gerenciador_db.conectar()  # Estabelecendo a conexão
    banco = Banco(gerenciador_db)  # Agora passando o gerenciador
    app = BancoApp(banco)
    app.iniciar()
except Exception as e:
    print(f"Ocorreu um erro: {e}")