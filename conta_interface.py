from abc import ABC, abstractmethod

class ContaInterface(ABC):

    @property
    @abstractmethod
    def saldo(self):
        """Retorna o saldo da conta."""
        pass

    @property
    @abstractmethod
    def titular(self):
        """Retorna o titular da conta."""
        pass

    @property
    @abstractmethod
    def tipo(self):
        """Retorna o tipo da conta."""
        pass

    @abstractmethod
    def depositar(self, valor: float):
        """Realiza um depósito na conta."""
        pass

    @abstractmethod
    def transferir(self, conta_destino: int, valor: float):
        """Realiza uma transferência para outra conta."""
        pass

    @abstractmethod
    def consultar_historico(self):
        """Consulta o histórico de transações da conta."""
        pass

    @abstractmethod
    def atualizar_saldo(self):
        """Atualiza o saldo da conta no banco de dados."""
        pass

    @abstractmethod
    def atualizar_saldo_apos_login(self, nome_titular):
        """Atualiza o saldo da conta no banco de dados após o login."""
        pass

    @abstractmethod
    def registrar_transacao(self, tipo_transacao, valor: float, conta_destino: int):
        """Registra uma transação no banco de dados."""
        pass

    @abstractmethod
    def cadastrar_chave_pix(self, chave, tipo):
        """Cadastra uma chave PIX na conta."""
        pass