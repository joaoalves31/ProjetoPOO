from titular import Titular 
from conta_interface import ContaInterface
from gerencia_banco_dados import filtro, escrever_arquivo, pegar_linhas_do_arquivo
import csv
import re
import uuid
from datetime import datetime

class Conta(ContaInterface):
    proximo_numero_conta = 666  # Variável de classe para manter o próximo número de conta
    pix_pendentes = {}  # Dicionário para armazenar códigos PIX pendentes

    def __init__(self, titular: "Titular", tipo: str, saldo: float = 0.0):
        # Definindo os atributos da conta
        self.numero_conta = Conta.proximo_numero_conta  # Atribuindo diretamente o número da conta
        Conta.proximo_numero_conta += 1
        self.__saldo = saldo if saldo is not None else 0.0
        self.__titular = titular
        
    @property
    def saldo(self):
        return self.__saldo 
    
    @saldo.setter
    def saldo(self, valor):
        if valor >= 0:
            super().saldo = valor
        else:
            raise ValueError("Saldo não pode ser negativo")
        
    @property
    def titular(self):
        return self.__titular

    @property
    def tipo(self):
        return self.__tipo

    def depositar(self, valor: float):
        if valor <= 0:
            raise ValueError("O valor do depósito deve ser maior que zero.")
        
        # Atualiza o saldo da conta
        self.__saldo += valor
        
        # Atualiza o saldo no arquivo de contas
        self.atualizar_saldo()
        
        # Registra a transação
        self.registrar_transacao("Depósito", valor)

    def concluir_pix_deposito(self, chave_pix: str) -> float:
        """Valida o PIX e conclui o depósito."""
        if not self.validar_pix(chave_pix):
            raise ValueError("Código PIX inválido ou já utilizado.")

        valor = self.pix_pendentes.pop(chave_pix)  # Remove e obtém o valor associado
        self.depositar(valor)
        return valor

    
    def gerar_pix_deposito(self, valor: float) -> str:
        """Gera um código PIX único para depósito e associa ao valor."""
        chave_pix = str(uuid.uuid4())  # Gera um código PIX único
        self.pix_pendentes[chave_pix] = valor
        return chave_pix
    
    def validar_pix(self, chave_pix: str) -> bool:
        """Verifica se a chave PIX é válida e não foi utilizada."""
        if chave_pix in self.pix_pendentes:
            return True
        return False

    def verificar_pix(self, codigo_pix: str) -> bool:
        """Verifica se o código PIX existe e retorna True se for associado a esta conta."""
        return codigo_pix in self.pix_pendentes

    def transferir(self, conta_destino: int = 0, valor: float = 0.1):
        if valor <= 0:
            raise ValueError("O valor da transferência deve ser maior que zero.")
        if valor > self.__saldo:
            raise ValueError("Saldo insuficiente para realizar a transferência.")
        
        # Realiza a transferência, subtraindo da conta origem e somando à conta destino
        self.__saldo -= valor
        
        # Atualiza o saldo da conta origem
        self.atualizar_saldo()
        
        # Recupera a conta destino
        conta_dest = filtro("contas.csv", 0, str(conta_destino), True)
        if conta_dest:
            conta_dest[0][2] = str(float(conta_dest[0][2]) + valor)
            escrever_arquivo("contas.csv", conta_dest[0])  # Atualiza a conta destino

        # Registra a transação
        self.registrar_transacao('Transferência', valor, conta_destino)

    def atualizar_saldo(self):
        # Lê todas as linhas do arquivo
        linhas = pegar_linhas_do_arquivo("contas.csv")
        
        for i, linha in enumerate(linhas):
            if linha[0] == str(self.numero_conta):  # Verifica o cpf
                linhas[i][2] = str(self.__saldo)  # Atualiza o saldo na terceira coluna
                break
        
        # Reescreve todas as linhas no arquivo
        try:
            with open("contas.csv", 'w', newline='', encoding='utf-8') as arquivo:
                writer = csv.writer(arquivo)
                writer.writerows(linhas)
        except Exception as e:
            print(f"Erro ao atualizar o saldo: {e}")

    def atualizar_saldo_apos_login(self, nome_titular):
        try:
            # Passo 1: Procurar o CPF no arquivo de titulares
            cpf_titular = None
            with open('titulares.csv', 'r') as f_titulares:
                reader = csv.reader(f_titulares)
                for linha in reader:
                    nome_arquivo = linha[0]  # Nome do titular
                    cpf_arquivo = linha[2]  # CPF do titular

                    if nome_arquivo.lower() == nome_titular.lower():
                        cpf_titular = cpf_arquivo
                        break
            
            if not cpf_titular:
                print(f"Titular '{nome_titular}' não encontrado no arquivo de titulares.")
                return None

            # Passo 2: Procurar o saldo no arquivo de contas usando o CPF
            with open('contas.csv', 'r') as f_contas:
                reader = csv.reader(f_contas)
                for linha in reader:
                    cpf_conta = linha[1]  # CPF da conta
                    saldo_conta = float(linha[2])  # Saldo da conta

                    if cpf_conta == cpf_titular:
                        self.__saldo = saldo_conta  # Atualiza o saldo diretamente
                        return self.saldo  # Use o getter

            print(f"Conta com CPF '{cpf_titular}' não encontrada no arquivo de contas.")
            return None

        except FileNotFoundError as e:
            print(f"Arquivo não encontrado: {e}")
            return None
        except Exception as e:
            print(f"Erro ao atualizar saldo: {e}")
            return None

    def registrar_transacao(self, descricao: str, valor: float = 0.1, conta_destino: int = None): 
        # Nomeia o arquivo de transações de forma global
        nome_arquivo = "transacoes.csv"  # Um único arquivo para todas as transações

        # Se nenhuma conta destino for informada, considera a própria conta
        if conta_destino is None:
            conta_destino = self.numero_conta

        # Obtém a data e hora atual
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Cria a transação com a data e hora
        transacao = [str(self.numero_conta), descricao, f"R$ {valor:.2f}", data_hora]

        # Escreve a transação no arquivo correspondente
        escrever_arquivo(nome_arquivo, transacao)


    def consultar_historico(self):
        transacoes = pegar_linhas_do_arquivo("transacoes.csv")
        historico = [t for t in transacoes if t[0] == str(self.numero_conta)]
        return historico


    def cadastrar_chave_pix(self, chave: str, tipo: str, numero_conta: str):
        nome_arquivo = "pix_registros.csv"
        linhas = pegar_linhas_do_arquivo(nome_arquivo)

        # Verifica se o arquivo existe ou precisa ser criado
        if not linhas:  # Se o arquivo estiver vazio (não existe), cria o arquivo
            linhas = [["chave", "tipo", "conta_associada"]]  # Cabeçalho

        # Verifica se a chave já está cadastrada
        for linha in linhas:
            if linha[0] == chave:
                print("Chave PIX já cadastrada!")
                return False

        # Valida a chave de acordo com o tipo
        if tipo == "CPF":
            if not self.validar_cpf(chave):
                print("CPF inválido!")
                return False
        elif tipo == "E-mail":
            if not self.validar_email(chave):
                print("E-mail inválido!")
                return False
        elif tipo == "Telefone":
            if not self.validar_telefone(chave):
                print("Número de telefone inválido!")
                return False
        else:
            print("Tipo de chave PIX inválido!")
            return False

        # Adiciona a chave, tipo e conta ao arquivo
        dados = [chave, tipo, numero_conta]
        escrever_arquivo(nome_arquivo, dados)  # Função já existente para adicionar ao arquivo

        return True
    
# Funções auxiliares para validação

def validar_email(self, email: str) -> bool:
        # Expressão regular para validar o e-mail
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_regex, email))

def validar_telefone(self, telefone: str) -> bool:
        # Expressão regular para validar o número de telefone (formato simples)
        telefone_regex = r'^\(\d{2}\)\s\d{4,5}-\d{4}$'
        return bool(re.match(telefone_regex, telefone))