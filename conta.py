import mysql.connector
from gerencia_banco_dados import gerencia_banco_dados 
from titular import Titular
from conta_interface import ContaInterface

class Conta(ContaInterface):
    proximo_numero_conta = 666  # Variável de classe para manter o próximo número de conta

    def __init__(self, titular: "Titular", tipo: str, saldo: float = 0.0):
        # Definindo os atributos da conta
        self.__tipo = tipo
        self._numero_conta = Conta.proximo_numero_conta
        Conta.proximo_numero_conta += 1
        self.__saldo = saldo if saldo is not None else 0.0
        self.__titular = titular

        # Conexão com o banco de dados
        self.db = gerencia_banco_dados(
            host='localhost',
            user='usuario_trabalho',
            password='senha_segura',
            database='banco_trabalho'
        )

    def get_numero_conta(self):
            return self._numero_conta
        
    @property
    def saldo(self):
        return self.__saldo 

    @property
    def titular(self):
        return self.__titular

    @property
    def numero_conta(self):
        return self.__numero_conta

    @property
    def tipo(self):
        return self.__tipo

    def depositar(self, valor: float = 0.1):
        """Realiza um depósito na conta e atualiza o banco de dados."""
        if valor <= 0:
            raise ValueError("O valor do depósito deve ser positivo.")
            
        self.__saldo += valor
        self.atualizar_saldo()  # Atualiza o saldo no banco
        self.registrar_transacao("depósito", valor)  # Registra a transação de depósito

    def transferir(self, conta_destino: int = 0, valor: float = 0.1):
        """Realiza uma transferência para outra conta e atualiza os saldos no banco de dados."""
        if valor <= 0:
            raise ValueError("O valor da transferência deve ser positivo.")
        if self.__saldo < valor:
            raise ValueError("Saldo insuficiente para a transferência.")
            
        # Atualiza o saldo da conta origem
        self.__saldo -= valor
        self.atualizar_saldo()  # Atualiza o saldo da conta origem no banco
            
        # Realiza o depósito na conta destino
        conta_destino.depositar(valor)  # Chama o método de depósito da conta destino
            
        # Registra a transação de transferência
        self.registrar_transacao("transferência", valor, conta_destino.numero_conta)

    def atualizar_saldo(self):
        """Atualiza o saldo da conta no banco de dados."""
        if self.db.conexao is None or not self.db.conexao.is_connected():
            self.db.conectar()  # Conectar caso a conexão não esteja aberta
        comando = "UPDATE contas SET saldo = %s WHERE numero_conta = %s"
        parametros = (self.__saldo, self.__numero_conta)
        self.db.executar_comando(comando, parametros)

    def registrar_transacao(self, tipo_transacao, valor: float = 0.1, conta_destino:int = 0):
        """Registra uma nova transação no banco de dados."""
        if self.db.conexao is None or not self.db.conexao.is_connected():
            self.db.conectar()  # Conectar caso a conexão não esteja aberta
        comando = """
        INSERT INTO transacoes (tipo_transacao, valor, conta_origem, conta_destino) 
        VALUES (%s, %s, %s, %s)
        """
        parametros = (tipo_transacao, valor, self.__numero_conta, conta_destino)
        self.db.executar_comando(comando, parametros)

    def consultar_historico(self):
        """Consulta o histórico de transações da conta no banco de dados."""
        if self.db.conexao is None or not self.db.conexao.is_connected():
            self.db.conectar()  # Conectar caso a conexão não esteja aberta
        comando = "SELECT * FROM transacoes WHERE conta_origem = %s OR conta_destino = %s"
        parametros = (self.__numero_conta, self.__numero_conta)
        historico = self.db.consultar_dados(comando, parametros)
        return historico