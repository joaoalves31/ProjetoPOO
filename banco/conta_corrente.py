from conta_bancaria import ContaBancaria, Titular
        
class ContaCorrente(ContaBancaria):
    def __init__(self, saldo: float, titular: Titular, numero_conta: int, limite: float):
        super().__init__(saldo, titular, numero_conta, tipo="Corrente")
        self.limite = limite

    def aplicar_limite(self,limite):
        pass