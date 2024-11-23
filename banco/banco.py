from conta_corrente import ContaCorrente
from conta_poupanca import ContaPoupanca
from titular import Titular

class Banco:
    def __init__(self):
        self.contas=[] #Lista com todas as contas do banco

    #Adiciona a conta ao final da lista Contas
    def adicionar_conta(self,conta) -> None:
        self.contas.append(conta)

    #Verifica se a conta esta dentro da lista, se sim remove ela
    def remover_conta(self,numero_conta:int) -> None:
        conta = self.procurar_conta(numero_conta)
        if conta:
            self.contas.remove(conta)
            print(f"Conta de número {numero_conta} removida com sucesso.")
        else:
            print(f"Conta com o número {numero_conta} não encontrada.")
    
    #Verifica se a conta esta na lista
    def procurar_conta(self,numero_conta:int):
        for conta in self.contas:
            if conta.numero_conta == numero_conta:
                return conta
        print(f"Conta com o número {numero_conta} não encontrada.")
        return None

    def autenticar_titular(self,login:str,senha:str):
        pass