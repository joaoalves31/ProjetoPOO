from conta import Conta

class ContaPoupanca(Conta):
    def __init__(self, saldo, titular, numero_conta, tipo, juros):
        super().__init__(saldo, titular, numero_conta, tipo)
        self.__juros = juros

    @property
    def juros(self):
        return self.__juros

    def aplicar_juros(self):
        # Implementação específica para aplicar juros
        self.__saldo += self.__saldo * self.__juros / 100
        self.atualizar_saldo()
