from conta import Conta
# Classe ContaPoupanca que herda Conta
class ContaPoupanca(Conta):
    def __init__(self, titular, tipo='ContaPoupanca', saldo = 0.0, juros=0.0):
        super().__init__(titular, tipo, saldo)
        self.__juros = juros

    def sacar(self, valor):
        if valor <= self.get_saldo():
            self.set_saldo(self.get_saldo() - valor)
            return True
        return False
