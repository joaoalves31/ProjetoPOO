import tkinter as tk
from tkinter import ttk, messagebox
from banco import Banco
from conta import Conta
from pessoa import Pessoa
from titular import Titular
from conta_corrente import ContaCorrente
from conta_poupanca import ContaPoupanca
from gerencia_banco_dados import filtro

# Interface gráfica com tkinter
class BancoApp:
    def __init__(self, banco):
        self.banco = banco
        self.transacoes = []  # Lista para armazenar as transações
        #self.diretorio_dados = banco.diretorio_dados
        self.root = tk.Tk()
        self.root.geometry("500x400")
        self.root.title("Sistema Bancário")
        self.root.configure(bg="#34495e")
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#ecf0f1", font=("Helvetica", 12))
        style.configure("TButton", background="#3498db", font=("Helvetica", 10, "bold"), padding=10)
        style.map("TButton", background=[("active", "#2980b9")])

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

        if not login or not senha:
            messagebox.showerror("Erro", "Login ou senha não podem estar vazios.")
            return

        # Buscar dados do titular no arquivo de titulares
        dados_titular = filtro("titulares.csv", numero_coluna=3, arg=login, retornar_uma_linha=True)
        
        if dados_titular:
            nome, idade, cpf, login_arquivo, senha_armazenada = dados_titular[0]  # Pega a primeira linha encontrada
            
            # Verificar a senha
            if senha == senha_armazenada:
                messagebox.showinfo("Sucesso", f"Bem-vindo(a), {nome}!")
                
                # Agora vamos buscar o saldo da conta
                self.numero_conta = login_arquivo  # Assumindo que login_arquivo seja o número da conta
                self.cpf = cpf  # CPF associado ao titular
                conta = self.banco.procurar_conta_por_cpf(cpf)
                # Atualiza o saldo da conta após o login
                conta.atualizar_saldo_apos_login(nome)
                
                self.tela_principal(conta)  # Exibe a tela principal com o saldo atualizado
            else:
                messagebox.showerror("Erro", "Senha incorreta.")
        else:
            messagebox.showerror("Erro", "Login não encontrado.")


    def tela_criar_conta(self):
        if not hasattr(self, 'tipo_conta_var'):
            self.tipo_conta_var = tk.StringVar(value="ContaCorrente")

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

        tk.Radiobutton(frame, text="Corrente", variable=self.tipo_conta_var, value="ContaCorrente", bg="#ecf0f1").grid(row=5, column=1, sticky="w")
        tk.Radiobutton(frame, text="Poupança", variable=self.tipo_conta_var, value="ContaPoupanca", bg="#ecf0f1").grid(row=6, column=1, sticky="w")

        ttk.Button(frame, text="Criar", command=self.criar_conta).grid(row=7, columnspan=2, pady=10)
        ttk.Button(frame, text="Voltar", command=self.tela_login).grid(row=8, columnspan=2, pady=5)

    def criar_conta(self):
        nome = self.nome_entry.get().strip()
        idade = self.idade_entry.get().strip()
        cpf = self.cpf_entry.get().strip()
        login = self.novo_login_entry.get().strip()
        senha = self.nova_senha_entry.get().strip()
        tipo = self.tipo_conta_var.get()

        if not nome.isalpha():
            messagebox.showerror("Erro", "O nome deve conter apenas letras.")
            return

        if not idade.isdigit() or not (18 <= int(idade) <= 100):
            messagebox.showerror("Erro", "Idade inválida.")
            return

        if not cpf or not login or not senha:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios.")
            return
        
        # Criação do objeto Titular
        titular = Titular(nome, idade, cpf, login, senha)
        #conta = Conta(titular, tipo, saldo = 0)
    
        mensagem = self.banco.adicionar_conta(titular, tipo)
        if mensagem == "Conta criada com sucesso!":
            messagebox.showinfo("Sucesso", mensagem)
            self.tela_login()
        else:
            messagebox.showerror("Erro", mensagem)

    def tela_principal(self, conta: Conta):
            if conta is None:
                messagebox.showerror("Erro", "Conta não encontrada.")
                return
            
            for widget in self.root.winfo_children():
                widget.destroy()

            frame = tk.Frame(self.root, bg="#ecf0f1", padx=20, pady=20)
            frame.pack(expand=True)

            titular_nome = conta.titular.nome
            print(f"Nome do titular: {titular_nome}")  # Para depuração
            saldo = conta.atualizar_saldo_apos_login(titular_nome)

            if saldo is not None:
                ttk.Label(frame, text=f"Bem-vindo(a), {titular_nome}!", font=("Helvetica", 14)).pack(pady=10)
                ttk.Label(frame, text=f"Saldo: R$ {saldo:.2f}").pack(pady=5)
            else:
                ttk.Label(frame, text="Erro ao carregar saldo.").pack(pady=5)

            ttk.Button(frame, text="Depositar", command=lambda: self.tela_depositar(conta)).pack(pady=5)
            ttk.Button(frame, text="Transferir", command=lambda: self.tela_transferir(conta)).pack(pady=5)
            ttk.Button(frame, text="Histórico", command=lambda: self.tela_historico(conta)).pack(pady=5)
            ttk.Button(frame, text="Cadastrar Chave PIX", command=lambda: self.cadastrar_chave_pix_tela(conta)).pack(pady=5)
            ttk.Button(frame, text="Sair", command=self.encerrar_sessao).pack(pady=10)

    def cadastrar_chave_pix_tela(self, conta: Conta):
        """
        Função para exibir a tela de cadastro da chave PIX e cadastrar a chave
        """
        cadastro_window = tk.Toplevel(self.root)
        cadastro_window.title("Cadastrar Chave PIX")
        cadastro_window.geometry("400x250")

        # Variáveis para armazenar as entradas
        chave_var = tk.StringVar()
        tipo_var = tk.StringVar()

        def cadastrar():
            chave = chave_var.get()
            tipo = tipo_var.get()
            numero_conta = conta.numero_conta  # Conta associada
            
            if chave and tipo:
                sucesso = conta.cadastrar_chave_pix(chave, tipo, numero_conta)
                if sucesso:
                    messagebox.showinfo("Sucesso", "Chave PIX cadastrada com sucesso!")
                else:
                    messagebox.showerror("Erro", "Falha ao cadastrar chave PIX.")
            else:
                messagebox.showerror("Erro", "Todos os campos precisam ser preenchidos.")

        # Labels e entradas
        ttk.Label(cadastro_window, text="Digite a chave PIX:").pack(pady=5)
        ttk.Entry(cadastro_window, textvariable=chave_var).pack(pady=5)

        ttk.Label(cadastro_window, text="Escolha o tipo de chave:").pack(pady=5)
        tipo_combobox = ttk.Combobox(cadastro_window, textvariable=tipo_var, values=["CPF", "Telefone", "E-mail"])
        tipo_combobox.pack(pady=5)
        tipo_combobox.set("CPF")  # Valor inicial

        # Botão para cadastrar
        ttk.Button(cadastro_window, text="Cadastrar", command=cadastrar).pack(pady=10)
        ttk.Button(cadastro_window, text="Cancelar", command=cadastro_window.destroy).pack(pady=5)

    def encerrar_sessao(self):
        resposta = messagebox.askyesno("Sair", "Tem certeza que deseja sair?")
        if resposta:
            # Retorna para a tela de login
            for widget in self.root.winfo_children():
                widget.destroy()
            self.tela_login()  # Volta à tela de login

    def tela_depositar(self, conta: Conta):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg="#ecf0f1", padx=20, pady=20)
        frame.pack(expand=True)

        ttk.Label(frame, text="Depósito", font=("Helvetica", 16)).pack(pady=10)

        ttk.Label(frame, text="Valor a depositar:").pack(pady=5)
        valor_entry = ttk.Entry(frame)
        valor_entry.pack(pady=5)

        def realizar_deposito():
            try:
                valor = float(valor_entry.get())
                if valor <= 0:
                    raise ValueError("O valor deve ser maior que zero.")

                # Chamando o método depositar da classe Conta
                conta.depositar(valor)

                messagebox.showinfo("Sucesso", f"Depósito de R$ {valor:.2f} realizado com sucesso!")
                self.tela_principal(conta)

            except ValueError as ve:
                messagebox.showerror("Erro", str(ve))

        ttk.Button(frame, text="Confirmar", command=realizar_deposito).pack(pady=10)
        ttk.Button(frame, text="Voltar", command=lambda: self.tela_principal(conta)).pack(pady=5)

    def tela_transferir(self, conta):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg="#ecf0f1", padx=20, pady=20)
        frame.pack(expand=True)

        ttk.Label(frame, text="Transferência", font=("Helvetica", 16)).pack(pady=10)

        ttk.Label(frame, text="CPF do destinatário:").pack(pady=5)
        cpf_entry = ttk.Entry(frame)
        cpf_entry.pack(pady=5)

        ttk.Label(frame, text="Valor a transferir:").pack(pady=5)
        valor_entry = ttk.Entry(frame)
        valor_entry.pack(pady=5)

        def realizar_transferencia():
            cpf_destinatario = cpf_entry.get().strip()
            try:
                valor = float(valor_entry.get())
                if valor <= 0:
                    raise ValueError("O valor deve ser maior que zero.")

                # Procurar conta do destinatário
                conta_destinatario = Conta.procurar_conta(cpf_destinatario)
                if not conta_destinatario:
                    raise ValueError("Conta do destinatário não encontrada.")

                # Verificar e realizar saque
                if not conta.sacar(valor):
                    raise ValueError("Saldo insuficiente.")

                # Depositar na conta do destinatário
                conta_destinatario.depositar(valor)

                # Atualizar saldos nos arquivos
                conta.atualizar_saldo()
                conta_destinatario.atualizar_saldo()

                # Registrar transações
                conta.registrar_transacao(f"Transferência de R$ {valor:.2f} para {cpf_destinatario}", valor)
                conta_destinatario.registrar_transacao(f"Recebimento de R$ {valor:.2f} da conta de {conta.titular}", valor)

                messagebox.showinfo("Sucesso", f"Transferência de R$ {valor:.2f} para {cpf_destinatario} realizada com sucesso!")
                self.tela_principal(conta)
            except ValueError as ve:
                messagebox.showerror("Erro", str(ve))

        ttk.Button(frame, text="Confirmar", command=realizar_transferencia).pack(pady=10)
        ttk.Button(frame, text="Voltar", command=lambda: self.tela_principal(conta)).pack(pady=5)



if __name__ == "__main__":
    # Suponha que os arquivos sejam 'titulares.csv' e 'contas.csv'
    banco = Banco('titulares.csv', 'contas.csv')  # Passando os dois arquivos para o Banco

    # Criação da interface do aplicativo (BancoApp)
    app = BancoApp(banco)
    
    # Inicializar a interface gráfica
    app.root.mainloop()

