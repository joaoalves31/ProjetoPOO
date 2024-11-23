from conta_bancaria import ContaBancaria, Titular

class ContaPoupanca(ContaBancaria):
    def __init__(self, saldo: float, titular: Titular, numero_conta: int, juros: float):
        super().__init__(saldo, titular, numero_conta, tipo="Poupança")
        self.juros = juros

    def aplicar_juros(self,juros):
        pass