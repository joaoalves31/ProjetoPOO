from conta_corrente import ContaCorrente
from conta_poupanca import ContaPoupanca

Class Cliente:
    def __init__(self, nome: str, cpf: str):
    self.nome = nome
    self.cpf = cpf

def criar_conta(self, tipo: str):
    if tipo == "corrente":
        return ContaCorrente(numero=0, titular=self.nome)
    elif tipo == "poupanca":
        return ContaPoupanca(numero=0, titular=self.nome)
    else:
        print("Tipo inválido de conta!")
        return None
    
    #Nome e saldo padrão, so para testar durante o desenvolvimento
