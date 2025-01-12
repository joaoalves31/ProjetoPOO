from conta import Conta
from gerencia_banco_dados import filtro, escrever_arquivo, pegar_linhas_do_arquivo
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
    
    def transferir(self, pix_destino: int = 0, valor: float = 0.1):
        if valor <= 0:
            raise ValueError("O valor da transferência deve ser maior que zero.")
        if valor > self.__saldo:
            raise ValueError("Saldo insuficiente para realizar a transferência.")
        
        # Realiza a transferência, subtraindo da conta origem e somando à conta destino
        self.__saldo -= valor
        
        # Atualiza o saldo da conta origem
        self.atualizar_saldo()
        
        # Recupera a conta destino pelo pix
        conta_pix = filtro("pix_registros.csv", 0, str(pix_destino), True )

        # Recupera a conta destino
        conta_dest = filtro("contas.csv", 0, str(conta_pix[0][2]), True)
        
        if conta_dest:
            conta_dest[0][2] = str(float(conta_dest[0][2]) + valor)
            escrever_arquivo("contas.csv", conta_dest[0])  # Atualiza a conta destino

        return True
