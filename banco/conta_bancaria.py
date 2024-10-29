class ContaBancaria:
    def __init__ (self, numero: int, titular:str, saldo: float = 0.0):
        self.numero = numero
        self.titular = titular
        self.saldo = saldo