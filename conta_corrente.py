from conta import Conta
from titular import Titular

class ContaCorrente(Conta):
    def __init__(self, titular, saldo=0.0, limite=500):
        super().__init__(titular, "ContaCorrente", saldo)  # Remove o argumento inválido
        self._limite = limite

    def get_limite(self):
        return self.__limite

    @property
    def limite(self):
        return self.__limite

    def aplicar_limite(self):
        # Implementação específica para aplicar limite
        pass