from titular import Titular
from conta import Conta
from gerencia_banco_dados import filtro, escrever_arquivo, pegar_linhas_do_arquivo
from conta_corrente import ContaCorrente
from conta_poupanca import ContaPoupanca
import csv

class Banco:
    def __init__(self, arquivo_titulares: str, arquivo_contas: str):
            self.arquivo_titulares = arquivo_titulares
            self.arquivo_contas = arquivo_contas

    def adicionar_conta(self, titular: Titular, tipo_conta: str):
        # Verifica se o titular já existe
        titular_existente = filtro(self.arquivo_titulares, 2, titular.cpf, True)
        if titular_existente:
            return "Titular já cadastrado com este CPF."

        # Define a classe correta com base no tipo de conta
        if tipo_conta == "ContaCorrente":
            nova_conta = ContaCorrente(titular)
        elif tipo_conta == "ContaPoupanca":
            nova_conta = ContaPoupanca(titular)
        else:
            return "Tipo de conta inválido."

        # Lê as linhas do arquivo de contas para verificar o último número de conta
        linhas = pegar_linhas_do_arquivo(self.arquivo_contas)
        ultimo_numero_conta = 0  # Caso o arquivo esteja vazio

        for linha in reversed(linhas):
            if linha and linha[0].isdigit():  # Verifica se a linha não está vazia e o primeiro valor é um número
                ultimo_numero_conta = int(linha[0])  # O número da conta está na primeira coluna
                break

        novo_numero_conta = ultimo_numero_conta + 1  # Incrementa 1 no último número de conta

        # Atualiza o número da conta da nova conta
        nova_conta.numero_conta = novo_numero_conta

        # Escreve os dados da nova conta no arquivo de contas
        dados_conta = [str(nova_conta.numero_conta), titular.cpf, f"{nova_conta.saldo:.2f}", f"{nova_conta.limite:.2f}" if isinstance(nova_conta, ContaCorrente) else "0.00"]
        print(f"Dados da conta para escrever: {dados_conta}")

        # Abre o arquivo de contas e escreve os dados
        try:
            with open(self.arquivo_contas, 'a', newline='', encoding='utf-8') as arquivo:
                writer = csv.writer(arquivo)
                writer.writerow(dados_conta)  # Escreve a nova conta no arquivo
        except Exception as e:
            print(f"Erro ao adicionar a conta: {e}")
            return "Erro ao adicionar a conta."

        # Salva o titular no arquivo
        dados_titular = [titular.nome, titular.idade, titular.cpf, titular.login, titular.senha]
        escrever_arquivo(self.arquivo_titulares, dados_titular)

        return "Conta criada com sucesso!"
    
    def procurar_conta_por_cpf(self, cpf):
        # Procurar pelo CPF na segunda coluna (índice 1)
        conta_dados = filtro(self.arquivo_contas, 1, cpf, True)
        
        if conta_dados:
            # Acessando os dados da conta
            tipo_conta = conta_dados[0][2]  # Tipo da conta (Corrente ou Poupança)
            saldo = float(conta_dados[0][3])  # Saldo da conta (convertido para float)
            
            # Localizar o titular da conta pelo CPF
            titular = self.procurar_titular_por_cpf(cpf)
            
            if titular:
                # Criando a instância da conta de acordo com o tipo
                if tipo_conta == "ContaCorrente":
                    return ContaCorrente(titular, saldo=saldo)
                elif tipo_conta == "ContaPoupanca":
                    return ContaPoupanca(titular, saldo=saldo)
                else:
                    return Conta(titular, tipo_conta, saldo)
        
        return None

    def procurar_titular_por_cpf(self, cpf):
        titular_dados = filtro(self.arquivo_titulares, 2, cpf, True)
        if titular_dados:
            # Instanciando o objeto Titular a partir dos dados
            nome = titular_dados[0][0]
            idade = int(titular_dados[0][1])
            cpf = titular_dados[0][2]
            login = titular_dados[0][3]
            senha = titular_dados[0][4]
            
            # Aqui você deve retornar uma instância de Titular
            return Titular(nome, idade, cpf, login, senha)
        return None

    def procurar_conta_por_pix(self, pix):
        # Procurar pelo pix
        conta_pix = filtro("pix_registros.csv", 0, pix, True)
        conta_dados = filtro(self.arquivo_contas, 0, conta_pix[0][2], True) #conta_dados[0][2] é o numero da conta
        
        if conta_dados:
            # Acessando os dados da conta
            tipo_conta = conta_dados[0][2]  # Tipo da conta (Corrente ou Poupança)
            saldo = float(conta_dados[0][3])  # Saldo da conta (convertido para float)
            
            # Localizar o titular da conta pelo CPF
            titular = self.procurar_titular_por_cpf(conta_dados[0][1])
            
            if titular:
                # Criando a instância da conta de acordo com o tipo
                if tipo_conta == "ContaCorrente":
                    return ContaCorrente(titular, saldo=saldo)
                elif tipo_conta == "ContaPoupanca":
                    return ContaPoupanca(titular, saldo=saldo)
                else:
                    return Conta(titular, tipo_conta, saldo)
        
        return None   