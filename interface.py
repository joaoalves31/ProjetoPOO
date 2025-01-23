import tkinter as tk
import customtkinter as ctk
import csv
from banco import Banco
from conta import Conta
from pessoa import Pessoa
from titular import Titular
from conta_corrente import ContaCorrente
from conta_poupanca import ContaPoupanca
from gerencia_banco_dados import filtro, buscar_conta_por_cpf, buscar_limite_por_cpf
from cpf_verificacao import validar_cpf, cpf_existe
from tkinter import ttk, messagebox
import re
# Interface gráfica com tkinter
class BancoApp:
    def __init__(self, banco):
        self.banco = banco
        self.transacoes = []  
        self.root = tk.Tk()
        self.root.geometry("400x700")
        self.root.title("Seu Banco")
        self.root.configure(bg="#f8f9fa")

        ctk.set_appearance_mode("Dark")  
        ctk.set_default_color_theme("blue")

        self.tela_boas_vindas()

    def tela_boas_vindas(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Frame principal com fundo branco
        frame = ctk.CTkFrame(self.root, fg_color="#ffffff")
        frame.pack(expand=True, padx=40, pady=40)

        # Rótulo principal com fonte Roboto
        ctk.CTkLabel(
            frame,
            text="Bem-vindo ao Seu Banco!",
            font=("Roboto", 24, "bold"),
            text_color="#2c3e50"
        ).pack(pady=20)

        # Rótulo secundário com fonte Roboto
        ctk.CTkLabel(
            frame,
            text="Gerencie suas finanças de forma segura e prática.",
            font=("Roboto", 14),
            text_color="#7f8c8d",
            wraplength=250,
            justify="center"
        ).pack(pady=10)

        # Botões com fonte Roboto e cantos arredondados
        ctk.CTkButton(
            frame,
            text="Login",
            command=self.tela_login,
            height=50,
            width=200,
            corner_radius=10,
            font=("Roboto", 14)
        ).pack(pady=20)

        ctk.CTkButton(
            frame,
            text="Criar Conta",
            command=self.tela_criar_conta,
            height=50,
            width=200,
            corner_radius=10,
            font=("Roboto", 14)
        ).pack(pady=10)

    def tela_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create the main frame with increased padding and rounded corners
        frame = ctk.CTkFrame(self.root, fg_color="#ffffff", corner_radius=20)
        frame.pack(expand=True, padx=50, pady=60)  # Increased padding

        # Login title label
        ctk.CTkLabel(
            frame,
            text="Acesse sua conta",
            font=("Roboto", 18, "bold"),
            text_color="#34495e"
        ).pack(pady=40)

        # Login label
        ctk.CTkLabel(
            frame,
            text="Login",
            text_color="#34495e",
            font=("Roboto", 14, "bold")
        ).pack(pady=5)

        # Login entry field
        self.login_entry = ctk.CTkEntry(
            frame,
            width=250,
            font=("Roboto", 12),
            placeholder_text="Digite seu login",
            fg_color="#ffffff",  # White background
            text_color="#2980b9"   # Blue text
        )
        self.login_entry.pack(pady=10)

        # Password label
        ctk.CTkLabel(
            frame,
            text="Senha",
            text_color="#34495e",
            font=("Roboto", 14, "bold")
        ).pack(pady=5)

        # Password entry field with asterisk masking
        self.senha_entry = ctk.CTkEntry(
            frame,
            width=250,
            show="*",
            font=("Roboto", 12),
            placeholder_text="Digite sua senha",
            fg_color="#ffffff",  # White background
            text_color="#2980b9"   # Blue text
        )
        self.senha_entry.pack(pady=10)

        # Feedback label (initially empty)
        self.feedback_label = ctk.CTkLabel(
            frame,
            text="",
            font=("Roboto", 12)
        )
        self.feedback_label.pack(pady=5)

        # Login button
        ctk.CTkButton(
            frame,
            text="Entrar",
            command=self.verificar_login,
            width=100,
            height=40,
            corner_radius=10,
            font=("Roboto", 14)
        ).pack(pady=20)

        # Voltar button
        ctk.CTkButton(
            frame,
            text="Voltar",
            command=self.tela_boas_vindas,
            width=100,
            height=30,
            corner_radius=10,
            font=("Roboto", 14)
        ).pack(pady=10)

        self.root.bind("<Return>", lambda event: self.verificar_login())

    def tela_criar_conta(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Frame principal
        frame = ctk.CTkFrame(self.root, fg_color="#ffffff", corner_radius=15)
        frame.pack(expand=True, padx=20, pady=20)

        # Título
        ctk.CTkLabel(
            frame, 
            text="Crie sua conta", 
            font=("Roboto", 18, "bold"), 
            text_color="#34495e"
        ).pack(pady=20)

        # Campo Nome
        ctk.CTkLabel(
            frame, 
            text="Nome", 
            text_color="#2980b9", 
            font=("Roboto", 14, "bold")
        ).pack(pady=5)
        self.nome_entry = ctk.CTkEntry(
            frame, 
            width=200,  # Tamanho menor
            fg_color="#ffffff", 
            text_color="#2980b9",  
            font=("Roboto", 12), 
            placeholder_text="Digite seu nome completo"
        )
        self.nome_entry.pack(pady=8)

        # Campo Idade
        ctk.CTkLabel(
            frame, 
            text="Idade", 
            text_color="#2980b9", 
            font=("Roboto", 14, "bold")
        ).pack(pady=5)
        self.idade_entry = ctk.CTkEntry(
            frame, 
            width=200,  # Tamanho menor
            fg_color="#ffffff", 
            text_color="#2980b9", 
            font=("Roboto", 12), 
            placeholder_text="Digite sua idade"
        )
        self.idade_entry.pack(pady=8)

        # Campo CPF
        ctk.CTkLabel(
            frame, 
            text="CPF", 
            text_color="#2980b9", 
            font=("Roboto", 14, "bold")
        ).pack(pady=5)
        self.cpf_entry = ctk.CTkEntry(
            frame, 
            width=200,  # Tamanho menor
            fg_color="#ffffff", 
            text_color="#2980b9", 
            font=("Roboto", 12), 
            placeholder_text="Digite seu CPF"
        )
        self.cpf_entry.pack(pady=8)

        # Campo Login
        ctk.CTkLabel(
            frame, 
            text="Login", 
            text_color="#2980b9", 
            font=("Roboto", 14, "bold")
        ).pack(pady=5)
        self.novo_login_entry = ctk.CTkEntry(
            frame, 
            width=200,  # Tamanho menor
            fg_color="#ffffff", 
            text_color="#2980b9", 
            font=("Roboto", 12), 
            placeholder_text="Crie seu login"
        )
        self.novo_login_entry.pack(pady=8)

        # Campo Senha
        ctk.CTkLabel(
            frame, 
            text="Senha", 
            text_color="#2980b9", 
            font=("Roboto", 14, "bold")
        ).pack(pady=5)
        self.nova_senha_entry = ctk.CTkEntry(
            frame, 
            width=200,  # Tamanho menor
            fg_color="#ffffff", 
            text_color="#2980b9", 
            show="*", 
            font=("Roboto", 12), 
            placeholder_text="Crie uma senha"
        )
        self.nova_senha_entry.pack(pady=8)

        # Seletor de Tipo de Conta
        ctk.CTkLabel(
            frame, 
            text="Tipo de Conta", 
            text_color="#2980b9", 
            font=("Roboto", 14, "bold")
        ).pack(pady=5)
        self.tipo_conta_var = tk.StringVar(value="ContaCorrente")

        # Radio buttons ajustados
        radio_frame = ctk.CTkFrame(frame, fg_color="#ffffff")  # Frame para melhor organização
        radio_frame.pack(pady=5)

        ctk.CTkRadioButton(
            radio_frame, 
            text="Conta Corrente",
            text_color="#2980b9", 
            variable=self.tipo_conta_var, 
            value="ContaCorrente"
        ).pack(side="left", padx=10)
        ctk.CTkRadioButton(
            radio_frame, 
            text="Conta Poupança",
            text_color="#2980b9", 
            variable=self.tipo_conta_var, 
            value="ContaPoupanca"
        ).pack(side="left", padx=10)

        # Botões
        button_frame = ctk.CTkFrame(frame, fg_color="#ffffff")  # Novo frame para organização dos botões
        button_frame.pack(pady=15)

        # Botão Criar Conta
        ctk.CTkButton(
            button_frame, 
            text="Criar Conta", 
            command=self.criar_conta, 
            width=100,  # Ajuste de tamanho
            height=35, 
            corner_radius=10,
            font=("Roboto", 14)
        ).pack(side="left", padx=10)

        # Botão Voltar
        ctk.CTkButton(
            button_frame, 
            text="Voltar", 
            command=self.tela_boas_vindas,  # Método para retornar ao menu principal
            width=100,  # Ajuste de tamanho
            height=35, 
            corner_radius=10,
            font=("Roboto", 14),
        ).pack(side="left", padx=10)

    def criar_conta(self):
            nome = self.nome_entry.get().strip()
            idade = self.idade_entry.get().strip()
            cpf = self.cpf_entry.get().strip()
            login = self.novo_login_entry.get().strip()
            senha = self.nova_senha_entry.get().strip()
            tipo = self.tipo_conta_var.get()  

            # Validações
            if not re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$", nome.strip()):
                messagebox.showerror("Erro", "O nome deve conter apenas letras e espaços.")
                return

            if not idade.isdigit() or not (18 <= int(idade) <= 100):
                messagebox.showerror("Erro", "Idade inválida. Deve ser maior que 18 anos.")
                return

            if not validar_cpf(cpf):  # Função separada para validar CPF
                messagebox.showerror("Erro", "CPF inválido.")
                return

            if cpf_existe(cpf, "contas.csv"):  # Função para verificar se CPF já existe no arquivo
                messagebox.showerror("Erro", "CPF já cadastrado.")
                return

            if not cpf or not login or not senha:
                messagebox.showerror("Erro", "Todos os campos são obrigatórios.")
                return

            # Criação do objeto Titular
            titular = Titular(nome=nome, idade=int(idade), cpf=cpf, login=login, senha=senha)

            # Adiciona a conta no banco usando o método da classe Banco
            mensagem = self.banco.adicionar_conta(titular, tipo)
            if mensagem == "Conta criada com sucesso!":
                messagebox.showinfo("Sucesso", mensagem)
                self.tela_login()  # Redireciona para a tela de login
            else:
                messagebox.showerror("Erro", mensagem)

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
            messagebox.showerror("Erro", "Login não encontrado. Tente novamente!")


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
                ctk.CTkLabel(frame, text=f"Olá, {titular_nome}!", font=("Roboto", 16), text_color="#2c3e50").pack(pady=10)
                ctk.CTkLabel(frame, text=f"Saldo: R$ {saldo:.2f}\n", font=("Roboto", 16), text_color="#2c3e50").pack(pady=5)
                cpf = conta.titular.cpf
                limite = buscar_limite_por_cpf(cpf)
                if limite:
                    ctk.CTkLabel(frame, text=f"Limite: R$ {limite:.2f}\n", font=("Roboto", 16), text_color="#2c3e50").pack(pady=5)
            else:
                ctk.CTkLabel(frame, text="Erro ao carregar saldo.").pack(pady=5)

            ctk.CTkButton(frame, text="Depositar", command=lambda: self.tela_depositar(conta)).pack(pady=5)
            ctk.CTkButton(frame, text="Transferir", command=lambda: self.tela_transferir(conta)).pack(pady=5)
            ctk.CTkButton(frame, text="Histórico", command=lambda: self.tela_historico(conta)).pack(pady=5)
            ctk.CTkButton(frame, text="Ver Chaves PIX", command=lambda: self.tela_chaves_pix(conta)).pack(pady=5)
            ctk.CTkButton(frame, text="Cadastrar Chave PIX", command=lambda: self.cadastrar_chave_pix_tela(conta)).pack(pady=5)
            ctk.CTkButton(frame, text="Sair", command=self.encerrar_sessao).pack(pady=10)

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
                    cadastro_window.destroy()  # Fecha a janela após o cadastro bem-sucedido
                else:
                    messagebox.showwarning("Erro", "Chave PIX já cadastrada.")
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
            self.tela_boas_vindas()  # Volta à tela de login

    def obter_chaves_pix(cpf_ou_email):
        chaves_pix = []
        with open("pix_registros.csv", newline='') as arquivo_csv:
            leitor = csv.reader(arquivo_csv)
            for linha in leitor:
                chave, tipo, conta_associada = linha
                if tipo == "E-mail" and chave == cpf_ou_email:
                    chaves_pix.append(conta_associada)  # Adiciona o número da conta associado ao E-mail
                elif tipo == "CPF" and chave == cpf_ou_email:
                    chaves_pix.append(conta_associada)  # Adiciona o número da conta associado ao CPF
        return chaves_pix        

    def tela_chaves_pix(self, conta):
        # Verifica se o root (janela principal) existe antes de criar uma nova janela
        if hasattr(self, 'root'):  # Mudamos de 'master' para 'root'
            nova_janela = tk.Toplevel(self.root)  # Usando self.root ao invés de self.master
            nova_janela.title("Chaves PIX")
            nova_janela.geometry("400x300")
        else:
            print("Erro: root não foi definido corretamente.")
            return

        # Criar a lista de chaves Pix
        nome_titular = conta.titular.cpf 
        # Passo 1: Obter o número da conta associado ao CPF
        numero_conta = buscar_conta_por_cpf(nome_titular)
        chaves_pix = conta.buscar_chaves_pix(numero_conta)  # Obter as chaves Pix dessa conta

        if chaves_pix:
            listbox = tk.Listbox(nova_janela)
            for chave, tipo in chaves_pix:  # Considerando que 'chaves_pix' é uma lista de tuplas (chave, tipo)
                listbox.insert(tk.END, f"{tipo}: {chave}")
            listbox.pack(pady=20)
        else:
            label_nenhuma_chave = tk.Label(nova_janela, text="Nenhuma chave Pix cadastrada.")
            label_nenhuma_chave.pack(pady=10)

        # Botão de Voltar
        botao_voltar = ttk.Button(nova_janela, text="Voltar", command=nova_janela.destroy)
        botao_voltar.pack(pady=10)    

    def tela_depositar(self, conta: Conta):
        """Tela inicial para inserir o valor do depósito."""
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg="#ecf0f1", padx=20, pady=20)
        frame.pack(expand=True)

        ttk.Label(frame, text="Depósito via PIX", font=("Roboto", 16)).pack(pady=10)
        ttk.Label(frame, text="Insira o valor a depositar:").pack(pady=5)
        valor_entry = ttk.Entry(frame)
        valor_entry.pack(pady=5)

        def gerar_pix():
            try:
                valor = float(valor_entry.get())
                if valor <= 0:
                    raise ValueError("O valor do depósito deve ser maior que zero.")
                chave_pix = conta.gerar_pix_deposito(valor)
                self.tela_codigo_pix(conta, chave_pix, valor)
            except ValueError as e:
                messagebox.showerror("Erro", str(e))
        
        ttk.Button(frame, text="Confirmar", command=gerar_pix).pack(pady=10)
        ttk.Button(frame, text="Voltar", command=lambda: self.tela_principal(conta)).pack(pady=5)


    def tela_codigo_pix(self, conta: Conta, chave_pix: str, valor: float):
        """Tela que exibe o código PIX gerado e permite copiar."""
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg="#ecf0f1", padx=20, pady=20)
        frame.pack(expand=True)

        ttk.Label(frame, text="Código PIX Gerado", font=("Roboto", 16)).pack(pady=10)
        ttk.Label(frame, text=f"Valor: R$ {valor:.2f}").pack(pady=5)
        pix_label = ttk.Entry(frame)
        pix_label.insert(0, chave_pix)
        pix_label.config(state='readonly')
        pix_label.pack(pady=5)

        def copiar_pix():
            self.root.clipboard_clear()
            self.root.clipboard_append(chave_pix)
            self.root.update()
            messagebox.showinfo("Código PIX", "Código copiado para a área de transferência.")

        ttk.Button(frame, text="Copiar Código de confirmação", command=copiar_pix).pack(pady=5)
        ttk.Button(frame, text="Continuar Depósito", command=lambda: self.tela_validar_pix(conta)).pack(pady=5)
        ttk.Button(frame, text="Voltar", command=lambda: self.tela_principal(conta)).pack(pady=5)

    def tela_validar_pix(self, conta: Conta):
        """Tela para validar o código PIX e completar o depósito."""
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg="#ecf0f1", padx=20, pady=20)
        frame.pack(expand=True)

        ttk.Label(frame, text="Insira o Código de confirmação!", font=("Roboto", 12)).pack(pady=10)
        pix_entry = ttk.Entry(frame)
        pix_entry.pack(pady=5)

        def validar_deposito():
            chave_pix = pix_entry.get()
            if conta.verificar_pix(chave_pix):
                valor = conta.concluir_pix_deposito(chave_pix)
                messagebox.showinfo("Depósito Concluído", f"Depósito de R$ {valor:.2f} realizado com sucesso!")
                self.tela_principal(conta)
            else:
                messagebox.showerror("Erro", "Código PIX inválido ou já utilizado.")

        ttk.Button(frame, text="Confirmar", command=validar_deposito).pack(pady=10)
        ttk.Button(frame, text="Voltar", command=lambda: self.tela_principal(conta)).pack(pady=5)


    def tela_historico(self, conta : Conta):
        """Exibe o histórico de transações usando o nome do titular."""
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg="#ecf0f1", padx=20, pady=20)
        frame.pack(expand=True)

        ttk.Label(frame, text="Histórico de Transações", font=("Roboto", 16)).pack(pady=10)

        nome_titular = conta.titular.nome
        # Obter o histórico de transações usando o nome do titular
        historico = conta.consultar_historico_por_nome(nome_titular)
        
        if isinstance(historico, str):  # Mensagem de erro ou falta de transações
            ttk.Label(frame, text=historico).pack(pady=5)
        else:
            for transacao in historico:
                ttk.Label(frame, text=", ".join(transacao)).pack(anchor="w", pady=2)

        ttk.Button(frame, text="Voltar", command=lambda: self.tela_principal(conta)).pack(pady=10)

    def tela_transferir(self, conta):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg="#ecf0f1", padx=20, pady=20)
        frame.pack(expand=True)

        ttk.Label(frame, text="Transferência", font=("Roboto", 16)).pack(pady=10)
        ttk.Label(frame, text="PIX do destinatário:").pack(pady=5)
        pix_entry = ttk.Entry(frame)
        pix_entry.pack(pady=5)

        ttk.Label(frame, text="Valor a transferir:").pack(pady=5)
        valor_entry = ttk.Entry(frame)
        valor_entry.pack(pady=5)

        def realizar_transferencia(tipo_transferencia):
            pix_destinatario = pix_entry.get().strip()
            try:
                valor = float(valor_entry.get())
                if valor <= 0:
                    raise ValueError("O valor deve ser maior que zero.")
                
                conta_destinatario = self.banco.procurar_conta_por_pix(pix_destinatario)

                if not conta_destinatario:
                    raise ValueError("Conta do destinatário não encontrada.")
                if tipo_transferencia == "saldo" or not hasattr(conta, "limite"):
                    if not conta.transferir(pix_destinatario, valor):
                        raise ValueError("Saldo insuficiente.")
                elif tipo_transferencia == "limite":
                    if not conta.transferir(valor, conta_destinatario):
                        raise ValueError("Saldo e limite insuficientes.")

                 # Passo 1: Obter o número da conta associado ao CPF do titular
                numero_conta_remetente = buscar_conta_por_cpf(conta.titular.cpf)
                numero_conta_destinatario = buscar_conta_por_cpf(conta_destinatario.titular.cpf)
                
                if not numero_conta_remetente or not numero_conta_destinatario:
                    raise ValueError("Número da conta não encontrado.")

                conta.registrar_transacao(f"Transferência de R$ {valor:.2f} para {pix_destinatario}", valor, numero_conta_remetente)
                conta_destinatario.registrar_transacao(f"Recebimento de R$ {valor:.2f} da conta {numero_conta_remetente}", valor, numero_conta_destinatario)

                messagebox.showinfo("Sucesso", f"Transferência de R$ {valor:.2f} para {pix_destinatario} realizada com sucesso!")
                self.tela_principal(conta)
            except ValueError as ve:
                messagebox.showerror("Erro", str(ve))

        if isinstance(conta, ContaCorrente): #confere se é corrente(pix com saldo da conta e pix no crédito) ou poupança(apenas pix com o saldo da conta)
            ttk.Label(frame, text="Tipo de transferência:").pack(pady=5)
            ttk.Button(frame, text="Usar Saldo", command=lambda: realizar_transferencia("saldo")).pack(pady=5)
            ttk.Button(frame, text="Usar Limite", command=lambda: realizar_transferencia("limite")).pack(pady=5)
        else:
            ttk.Button(frame, text="Transferir", command=lambda: realizar_transferencia("saldo")).pack(pady=5)

        ttk.Button(frame, text="Voltar", command=lambda: self.tela_principal(conta)).pack(pady=5)


if __name__ == "__main__":
    # Suponha que os arquivos sejam 'titulares.csv' e 'contas.csv'
    banco = Banco('titulares.csv', 'contas.csv')  # Passando os dois arquivos para o Banco
    

    # Criação da interface do aplicativo (BancoApp)
    app = BancoApp(banco)
    
    # Inicializar a interface gráfica
    app.root.mainloop()