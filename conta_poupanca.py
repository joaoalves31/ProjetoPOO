from conta import Conta
from gerencia_banco_dados import filtro, escrever_arquivo, pegar_linhas_do_arquivo
# Classe ContaPoupanca que herda Conta
class ContaPoupanca(Conta):
    def __init__(self, titular, tipo='ContaPoupanca', saldo = 0.0, juros=0.0):
        super().__init__(titular, tipo, saldo)
        self.__juros = juros

    def depositar(self, valor: float = 0.1):
        super().depositar()    

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
        
        # Subtrai o valor da conta de origem
        self.__saldo -= valor
        self.atualizar_saldo()  # Atualiza o saldo da conta origem
        
        # Recupera a conta destino pelo pix
        conta_pix = filtro("pix_registros.csv", 0, str(pix_destino), True)
        if not conta_pix:
            raise ValueError("Conta PIX destino não encontrada.")
        
        # Recupera a conta destino
        conta_dest = filtro("contas.csv", 0, conta_pix[0][2], True)
        if conta_dest:
            # Atualiza diretamente o saldo na conta destino
            conta_dest[0][2] = str(float(conta_dest[0][2]) + valor)
            
            # Atualiza o saldo no arquivo
            self.atualizar_saldo_conta_destino(conta_dest[0])  # Passa a linha da conta destino para atualização
            
        return True
