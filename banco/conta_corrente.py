class ContaCorrente(ContaBancaria):
    def __init__ (self, numero: int, titular: str, saldo: float = 0.0, limite: float = 1000.0):
        super().__init__(numero, titular, saldo) # O super é usado para acessar atributos de uma classe pai por dentro de uma classe filha
        self.limite = limite #Esse é um novo atributo de uma conta corrente.
        