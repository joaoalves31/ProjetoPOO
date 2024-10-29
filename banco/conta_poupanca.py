from conta_bancaria import ContaBancaria

class ContaPoupanca(ContaBancaria):
    def __init__(self, numero: int, titular: str, saldo: float = 0.0, rendimento: float = 0.0): 
        super().__init__(numero, titular, saldo)
        self.juros = juros