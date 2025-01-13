import re

@staticmethod
def validar_cpf(cpf: str) -> bool:
    # Remove caracteres não numéricos
    cpf = re.sub(r'\D', '', cpf)

    # Verifica se o CPF tem 11 números
    if len(cpf) != 11:
        return False

    # Verifica se é uma sequência de números iguais (tipo 11111111111)
    if cpf == cpf[0] * len(cpf):
        return False

    # Calcula o 1º dígito de verificação
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma * 10 % 11) % 10
    if digito1 != int(cpf[9]):
        return False

    # Calcula o 2º dígito de verificação
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma * 10 % 11) % 10
    if digito2 != int(cpf[10]):
        return False

    return True

@staticmethod
def cpf_existe(cpf: str, nome_arquivo: str) -> bool:
    try:
        with open(nome_arquivo, 'r') as arquivo:
            for linha in arquivo:
                # Verifica se o CPF já existe na linha
                if cpf in linha:
                    return True
    except FileNotFoundError:
        print("Arquivo não encontrado.")

    return False
