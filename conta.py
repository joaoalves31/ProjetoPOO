from titular import Titular 
from conta_interface import ContaInterface
from gerencia_banco_dados import filtro, escrever_arquivo, pegar_linhas_do_arquivo, buscar_conta_por_cpf, buscar_numero_conta_por_cpf
import csv
import re
import uuid
from datetime import datetime
from cpf_verificacao import validar_cpf

class Conta(ContaInterface):
    proximo_numero_conta = 666  # Valor inicial padrão

    def __init__(self, titular: "Titular", tipo: str, saldo: float = 0.0):
        self.numero_conta = Conta.proximo_numero_conta
        Conta.proximo_numero_conta += 1
        self.__saldo = saldo if saldo is not None else 0.0
        self.__titular = titular 
        self.pix_pendentes = {}
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
        self.__saldo += valor
        
        self.atualizar_saldo()
        
        nome_titular = self.titular.cpf 

        numero_conta = buscar_conta_por_cpf(nome_titular)

        self.registrar_transacao("Depósito", valor, numero_conta)

    def concluir_pix_deposito(self, chave_pix: str) -> float:
        """Valida o PIX e conclui o depósito."""
        if not self.validar_pix(chave_pix):
            raise ValueError("Código PIX inválido ou já utilizado.")

        valor = self.pix_pendentes.pop(chave_pix) 
        self.depositar(valor)
        return valor

    
    def gerar_pix_deposito(self, valor: float) -> str:
        chave_pix = str(uuid.uuid4())  # Gera um código PIX único
        self.pix_pendentes[chave_pix] = valor
        return chave_pix
    
    def validar_pix(self, chave_pix: str) -> bool:
        if chave_pix in self.pix_pendentes:
            return True
        return False

    def verificar_pix(self, codigo_pix: str) -> bool:
        return codigo_pix in self.pix_pendentes
    

    def transferir(self, pix_destino: int = 0, valor: float = 0.1):
        if valor <= 0:
            raise ValueError("O valor da transferência deve ser maior que zero.")
        if valor > self.__saldo:
            raise ValueError("Saldo insuficiente para realizar a transferência.")
    
        self.__saldo -= valor
        self.atualizar_saldo()
        
        conta_pix = filtro("pix_registros.csv", 0, str(pix_destino), True)
        if not conta_pix:
            raise ValueError("Conta PIX destino não encontrada.")
        
        conta_dest = filtro("contas.csv", 0, conta_pix[0][2], True)
        if conta_dest:
            conta_dest[0][2] = str(float(conta_dest[0][2]) + valor)
            

            self.atualizar_saldo_conta_destino(conta_dest[0])  # Passa a linha da conta destino para atualização
            
        return True

    def atualizar_saldo(self):
        # Obtém o número da conta com base no CPF
        cpf_titular = self.titular.cpf  # Supondo que o CPF está armazenado na instância do titular
        numero_conta = buscar_numero_conta_por_cpf(cpf_titular)

        if numero_conta is None:
            print(f"Conta não encontrada para o CPF: {cpf_titular}")
            return

        # Lê todas as linhas do arquivo
        linhas = pegar_linhas_do_arquivo("contas.csv")

        for i, linha in enumerate(linhas):
            if linha[0] == str(numero_conta):  # Verifica o número da conta
                linha[2] = f"{self.__saldo:.2f}"  # Atualiza o saldo no formato string
                break
        else:
            print(f"Conta {numero_conta} não encontrada no arquivo.")

        # Reescreve todas as linhas no arquivo sem criar novas linhas
        try:
            with open("contas.csv", 'w', newline='', encoding='utf-8') as arquivo:
                for linha in linhas:
                    arquivo.write(','.join(linha) + '\n')  # Escreve as linhas como string CSV
        except Exception as e:
            print(f"Erro ao atualizar o saldo: {e}")

    def atualizar_saldo_conta_destino(self, conta_destino):
        # Carrega todas as linhas do arquivo "contas.csv"
        linhas = pegar_linhas_do_arquivo("contas.csv")  # Função que retorna as linhas do arquivo
        
        for i, linha in enumerate(linhas):
            # Verifica se a conta destino corresponde ao ID da conta
            if linha[0] == conta_destino[0]:  # O primeiro campo é o ID da conta
                linha[2] = str(conta_destino[2])  # Atualiza o saldo (o saldo está no índice 2)
                break  # Conta encontrada, atualizada e saída do loop

        # Reabre o arquivo "contas.csv" para sobrescrever com as linhas modificadas
        with open("contas.csv", 'w', newline='', encoding='utf-8') as arquivo:
            for linha in linhas:
                arquivo.write(','.join(linha) + '\n')  # Escreve cada linha novamente no arquivo

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

            # Passo 2: Usar o CPF para buscar o número da conta
            numero_conta = buscar_numero_conta_por_cpf(cpf_titular)

            if numero_conta is None:
                print(f"Conta não encontrada para o CPF: {cpf_titular}")
                return None

            # Passo 3: Procurar o saldo no arquivo de contas usando o número da conta
            with open('contas.csv', 'r') as f_contas:
                reader = csv.reader(f_contas)
                for linha in reader:
                    if linha[0] == str(numero_conta):  # Verifica o número da conta
                        self.__saldo = float(linha[2])  # Atualiza o saldo diretamente
                        return self.saldo  # Use o getter

            print(f"Conta com número '{numero_conta}' não encontrada no arquivo de contas.")
            return None

        except FileNotFoundError as e:
            print(f"Arquivo não encontrado: {e}")
            return None
        except Exception as e:
            print(f"Erro ao atualizar saldo: {e}")
            return None

    # Passando explicitamente o número da conta ao registrar a transação
    def registrar_transacao(self, descricao: str, valor: float = 0.1, conta_destino: int = None): 
        
        # Nomeia o arquivo de transações de forma global
        nome_arquivo = "transacoes.csv"  # Um único arquivo para todas as transações

        # Obtém a data e hora atual
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Cria a transação com a data e hora
        transacao = [str(conta_destino), descricao, f"R$ {valor:.2f}", data_hora]

        # Escreve a transação no arquivo correspondente
        escrever_arquivo(nome_arquivo, transacao)


    def consultar_historico_por_nome(self, nome_titular: str):
        """Consulta o histórico de transações usando o nome do titular."""
        try:
            # Passo 1: Obter o CPF associado ao nome do titular
            titulares = pegar_linhas_do_arquivo("titulares.csv")
            cpf = None
            for titular in titulares:
                if len(titular) >= 3 and titular[0] == nome_titular:  # Garantir que a linha tem pelo menos 3 colunas
                    cpf = titular[2]  # CPF está na terceira coluna
                    break
            if not cpf:
                return f"Titular '{nome_titular}' não encontrado."

            # Passo 2: Obter o número da conta associado ao CPF
            contas = pegar_linhas_do_arquivo("contas.csv")
            numero_conta = None
            for conta in contas:
                if len(conta) >= 2 and conta[1] == cpf:  # Garantir que a linha tem pelo menos 2 colunas
                    numero_conta = conta[0]  # Número da conta está na primeira coluna
                    break
            if not numero_conta:
                return f"Conta associada ao CPF '{cpf}' não encontrada."

            # Passo 3: Obter o histórico de transações usando o número da conta
            transacoes = pegar_linhas_do_arquivo("transacoes.csv")
            historico = [
                t for t in transacoes
                if len(t) >= 2 and t[0] == numero_conta  # Garantir que a linha tem pelo menos 2 colunas
            ]

            return historico if historico else f"Nenhuma transação encontrada para a conta '{numero_conta}'."

        except FileNotFoundError as e:
            return f"Erro: Arquivo não encontrado - {e.filename}"
        except Exception as e:
            return f"Erro inesperado: {str(e)}"

            return historico if historico else f"Nenhuma transação encontrada para a conta '{numero_conta}'."
        
    def cadastrar_chave_pix(self, chave: str, tipo: str, numero_conta: str):
        nome_arquivo = "pix_registros.csv"
        linhas = pegar_linhas_do_arquivo(nome_arquivo)

        # Verifica se o arquivo existe ou precisa ser criado
        if not linhas:  # Se o arquivo estiver vazio (não existe), cria o arquivo
            linhas = [["chave", "tipo", "conta_associada"]]  # Cabeçalho

        # Verifica se a chave já está cadastrada
        for linha in linhas:
            if linha[0] == chave:
                print(f"Chave PIX já cadastrada! Chave: {chave}")
                return False

        # Valida a chave de acordo com o tipo
        if tipo == "CPF":
            if not validar_cpf(chave):  # Agora usa a função importada
                print(f"CPF inválido! Chave fornecida: {chave}")
                return False
        elif tipo == "E-mail":
            if not self.validar_email(chave):
                print(f"E-mail inválido! Chave fornecida: {chave}")
                return False
        elif tipo == "Telefone":
            if not self.validar_telefone(chave):
                print(f"Número de telefone inválido! Chave fornecida: {chave}")
                return False
        else:
            print("Tipo de chave PIX inválido!")
            return False

        # Adiciona a chave, tipo e conta ao arquivo

        nome_titular = self.titular.cpf 
        # Passo 1: Obter o número da conta associado ao CPF
        numero_conta = buscar_conta_por_cpf(nome_titular)

        dados = [chave, tipo, numero_conta]
        escrever_arquivo(nome_arquivo, dados)  # Função já existente para adicionar ao arquivo

        print(f"Chave PIX cadastrada com sucesso: {dados}")  # Mensagem de sucesso
        return True
        
        # Funções auxiliares para validação

    def buscar_chaves_pix(self, numero_conta):
        """Retorna uma lista de chaves PIX cadastradas para o número de conta informado."""
        chaves = []
        try:
            with open("pix_registros.csv", mode="r") as file:
                reader = csv.reader(file)
                for row in reader:
                    print(f"Lendo linha: {row}")  # Depuração
                    if row[2] == str(numero_conta):  # Verifique se a comparação é com a terceira coluna
                        tipo_chave = row[1]
                        chave = row[0]
                        chaves.append((chave, tipo_chave))
        except FileNotFoundError:
            print("Arquivo pix_registros.csv não encontrado.")
            pass  # Se o arquivo não for encontrado, retorna lista vazia
        return chaves 
   

    def validar_email(self, email: str) -> bool:
            # Expressão regular para validar o e-mail
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            return bool(re.match(email_regex, email))

    def validar_telefone(self, telefone: str) -> bool:
        # Expressão regular para validar o número de telefone com ou sem formatação
        telefone_regex = r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$'
        return bool(re.match(telefone_regex, telefone))

    