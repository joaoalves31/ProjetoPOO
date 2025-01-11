import re

def validar_cpf(cpf: str) -> bool:
    # Remove caracteres não numéricos
    cpf = re.sub(r'\D', '', cpf)
    
    # Olha se o CPF tem 11 numeros

    if len(cpf) != 11:
        return False
    
    # Olha se é uma sequencia de numeros iguais (tipo 11111111111)
    if cpf == cpf[0] * len(cpf):
        return False
     
     # Calcula o 1º digito de verificação
    for i in range(9, 11):
        soma = sum(int(cpf[num]) * ((i + 1) - num) for num in range(0, i))
        digito = (soma * 10 % 11) % 10
        if digito != int(cpf[i]):
            return False
    
    return True

    # Calcula o 2º digito de verificação
def cpf_existe(cpf: str, nome_arquivo: str) -> bool:
    try:
        with open(nome_arquivo, 'r') as arquivo:
            for linha in arquivo:
                if cpf in linha:
                    return True
    except FileNotFoundError:
        print("Arquivo não encontrado.")
    
    return False