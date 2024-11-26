import mysql.connector
from mysql.connector import Error
import re
import hashlib
from pessoa import Pessoa
from titular import Titular
from conta import Conta
from gerencia_banco_dados import gerencia_banco_dados
from conta_corrente import ContaCorrente
from conta_poupanca import ContaPoupanca

class Banco:
    def __init__(self, gerenciador_db):
        self.gerenciador_db = gerenciador_db
        self.contas = self.carregar_contas()

    def carregar_contas(self):
        query = "SELECT numero_conta, saldo, tipo, titular_id, limite, juros FROM contas"
        contas_data = self.gerenciador_db.consultar_dados(query)

        contas = []
        for conta_data in contas_data:
            numero_conta, saldo, tipo, titular_id, limite, juros = conta_data

            # Recupera os dados do titular
            query = "SELECT nome, idade, cpf FROM pessoas WHERE id = %s"
            pessoa_data = self.gerenciador_db.consultar_dados(query, (titular_id,))
            nome, idade, cpf = pessoa_data[0] if pessoa_data else (None, None, None)

            query = "SELECT login, senha FROM titulares WHERE pessoa_id = %s"
            titular_data = self.gerenciador_db.consultar_dados(query, (titular_id,))
            login, senha = titular_data[0] if titular_data else (None, None)

            titular = Titular(nome, idade, cpf, login, senha)
            titular._Titular__id = titular_id  # Ajusta o ID do titular

            # Cria a conta dependendo do tipo
            if tipo == "ContaCorrente":
                limite = limite if limite is not None else 500  # Define limite padrão
                conta = ContaCorrente(saldo, titular, numero_conta, tipo, limite)
            elif tipo == "ContaPoupanca":
                juros = juros if juros is not None else 0.01
                conta = ContaPoupanca(saldo, titular, numero_conta, tipo, juros)
            else:
                conta = Conta(saldo, titular, numero_conta, tipo)

            contas.append(conta)

        return contas

    def adicionar_conta(self, nome: str, idade: int, cpf: str, login: str, senha: str, tipo: str, limite: float = 500, juros: float = 0.01):
        # Sincronizar o próximo ID com o banco
        query = "SELECT MAX(id) FROM pessoas"
        resultado = self.gerenciador_db.consultar_dados(query)

        # Garante que max_id seja um número, mesmo se o resultado for None
        max_id = resultado[0]['MAX(id)'] if resultado and resultado[0]['MAX(id)'] is not None else 0

        print(f"DEBUG: Resultado do SELECT MAX(id): {resultado}")  # Debug

        Pessoa.proximo_id = max_id + 1  # Ajusta o próximo ID para evitar duplicação

        # Verificar se o login já está em uso
        query = "SELECT login FROM titulares WHERE login = %s"
        login_existente = self.gerenciador_db.consultar_dados(query, (login,))

        if login_existente:
            print(f"DEBUG: O login '{login}' já está em uso.")
            return "O login já está em uso."

        # Criar instância de Pessoa e inserir no banco de dados
        pessoa = Pessoa(nome, idade, cpf)
        
        try:
            query = "INSERT INTO pessoas (id, nome, idade, cpf) VALUES (%s, %s, %s, %s)"
            self.gerenciador_db.executar_comando(query, (pessoa.get_id(), nome, idade, cpf))
        except mysql.connector.Error as err:
            print(f"Erro ao executar o comando: {err}")
            return f"Erro ao criar pessoa: {err}"

        # Criar instância de Titular e inserir no banco de dados
        titular = Titular(nome, idade, cpf, login, senha)
        
        try:
            query = "INSERT INTO titulares (id, login, senha, pessoa_id) VALUES (%s, %s, %s, %s)"
            self.gerenciador_db.executar_comando(query, (titular.get_id(), login, titular.hash_senha(senha), pessoa.get_id()))
        except mysql.connector.Error as err:
            print(f"Erro ao executar o comando: {err}")
            return f"Erro ao criar titular: {err}"

        # Criar instância de Conta e inserir no banco de dados
        if tipo == "ContaCorrente":
            nova_conta = ContaCorrente(titular=titular, saldo=0.0, limite=limite)
        elif tipo == "ContaPoupanca":
            nova_conta = ContaPoupanca(titular=titular, saldo=0.0, juros=juros)
        else:
            print(f"DEBUG: Tipo de conta inválido: {tipo}")
            return "Tipo de conta inválido."

        try:
            query = """
            INSERT INTO contas (numero_conta, saldo, tipo, titular_id, limite, juros)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            self.gerenciador_db.executar_comando(
                query, 
                (
                    nova_conta.get_numero_conta(), 
                    0.0, 
                    tipo, 
                    titular.get_id(), 
                    limite if tipo == "ContaCorrente" else None, 
                    juros if tipo == "ContaPoupanca" else None
                )
            )
        except mysql.connector.Error as err:
            print(f"Erro ao executar o comando: {err}")
            return f"Erro ao criar conta: {err}"

        # Atualizar a lista de contas em memória
        self.contas.append(nova_conta)
        return "Conta criada com sucesso!"

    def remover_conta(self, numero_conta):
    # Primeiro, recupera o titular_id associado à conta
        query = "SELECT titular_id FROM contas WHERE numero_conta = %s"
        resultado = self.gerenciador_db.consultar_dados(query, (numero_conta,))
        if not resultado:
            return "Conta não encontrada."

        titular_id = resultado[0][0]

        # Remove a conta
        query = "DELETE FROM contas WHERE numero_conta = %s"
        self.gerenciador_db.executar_comando(query, (numero_conta,))

        # Verifica se o titular tem outras contas
        query = "SELECT COUNT(*) FROM contas WHERE titular_id = %s"
        resultado = self.gerenciador_db.consultar_dados(query, (titular_id,))
        if resultado[0][0] == 0:
            # Se o titular não tem outras contas, remove o titular e a pessoa associada
            query = "DELETE FROM titulares WHERE id = %s"
            self.gerenciador_db.executar_comando(query, (titular_id,))

            query = "DELETE FROM pessoas WHERE id = %s"
            self.gerenciador_db.executar_comando(query, (titular_id,))

        # Atualiza a lista de contas em memória
        self.contas = [conta for conta in self.contas if conta.get_numero_conta() != numero_conta]

        return "Conta removida com sucesso."

    def procurar_conta_por_login(self, login: str):
        for conta in self.contas:
            if conta.titular.get_login() == login:  # Usa o getter para acessar o login
                return conta
        return None  # Se não encontrar nenhuma conta com esse login
