from conta import Conta
from titular import Titular

class ContaCorrente(Conta):
    def __init__(self, titular, tipo = 'ContaCorrente', saldo = 0.0, limite=0.0):
        super().__init__(titular, tipo, saldo)  # Chama o init da classe pai (Conta)
        self.__limite = limite

    @property
    def limite(self):
        return self.__limite
    
    @limite.setter
    def limite(self, valor):
        if valor >= 0:
            self.__limite = valor
        else:
            raise ValueError("Limite não pode ser negativo")
        
    @property
    def tipo(self):
        return 'corrente'  
    
    def depositar(self, valor: float = 0.1):
        super().depositar()
    
    def sacar(self, valor):
        if valor <= self.saldo + self.__limite:
            self.saldo(self.saldo() - valor)
            return True
        return False