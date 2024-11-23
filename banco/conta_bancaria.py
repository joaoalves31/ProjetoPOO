from titular import Titular
from abc import ABC, abstractmethod

class ContaBancaria(ABC):
    def __init__(self, saldo: float, titular: Titular, numero_conta: int, tipo: str):
        self.saldo = saldo
        self.titular = titular
        self.numero_conta = numero_conta
        self.tipo = tipo

    #Realiza o deposito na conta
    def depositar(self,valor:float) -> str:
        if valor <=0:
            return "Erro: O valor do depósito deve ser positivo."
        else:
            self.saldo += valor
            self.registrar_transacao("Deposito", valor)
            return f"Depósito de R${valor:.2f} realizado com sucesso."

    #Realiza uma transferencia entre contas bancarias
    def transferir(self,conta_destino,valor:float) -> str:
        if valor <= 0:
            return "Erro: O valor da transferencia deve ser positivo."
        elif valor > self.saldo:
            return "Saldo insuficiente para a transferência."
        else:
            self.saldo-=valor
            conta_destino.depositar(valor)
            self.registrar_transacao("Transferencia", valor, conta_destino)
            return f"Transferência de R${valor:.2f} para a conta {conta_destino.numero_conta}"
        
    def registrar_transacao(self,tipo_transacao:str,valor:float,conta_destino):
        pass
    
    def consultar_historico():
        pass