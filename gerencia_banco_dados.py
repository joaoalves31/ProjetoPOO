import csv
from typing import List

# Cria um novo arquivo com as linhas especificadas
def novo_arquivo(nome_arquivo: str, linhas: List[List[str]]) -> bool:
    try:
        with open(nome_arquivo, 'w', newline='', encoding='utf-8') as arquivo:
            writer = csv.writer(arquivo, delimiter=' ')
            for linha in linhas:
                writer.writerow(linha)
        return True
    except Exception as e:
        print(f"Erro ao escrever no arquivo: {e}")
        return False


# Remove as aspas duplas de uma string
def remove_aspas(texto_puro: str, i: int) -> str:
    texto = ""
    while i < len(texto_puro) and texto_puro[i] != '\"':
        texto += texto_puro[i]
        i += 1
    return texto

# Converte uma linha de texto em uma lista, separando os campos por vírgula
def converter_linha_para_lista(linha: str) -> List[str]:
    return linha.strip().split(',')


# Lê todas as linhas de um arquivo e retorna uma lista de listas
def pegar_linhas_do_arquivo(nome_arquivo: str) -> List[List[str]]:
    linhas = []
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                linhas.append(converter_linha_para_lista(linha.strip()))
    except FileNotFoundError:
        print(f"Arquivo {nome_arquivo} não encontrado.")
    return linhas


# Filtra as linhas do arquivo com base em uma coluna específica e um argumento
def filtro(nome_arquivo: str, numero_coluna: int, arg: str, retornar_uma_linha: bool) -> List[List[str]]:
    linhas = pegar_linhas_do_arquivo(nome_arquivo)
    linhas_filtradas = []

    for linha in linhas:
        print(f"Verificando linha: {linha}")  # Depuração
        if len(linha) > numero_coluna and linha[numero_coluna] == arg:
            linhas_filtradas.append(linha)
            if retornar_uma_linha:
                return linhas_filtradas

    print(f"Linhas filtradas: {linhas_filtradas}")  # Depuração
    return linhas_filtradas



# Escreve uma linha no arquivo (adicionando ao final)
def escrever_arquivo(nome_arquivo: str, dados: List[str]) -> None:
    try:
        with open(nome_arquivo, 'a', newline='', encoding='utf-8') as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow(dados)
    except Exception as e:
        print(f"Erro ao escrever no arquivo: {e}")


# Lê todas as linhas do arquivo e as retorna como uma lista de listas
def ler_arquivo(nome_arquivo: str) -> List[List[str]]:
    linhas = []
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            reader = csv.reader(arquivo)
            for linha in reader:
                linhas.append(linha)
    except FileNotFoundError:
        print(f"Arquivo {nome_arquivo} não encontrado.")
    return linhas



def buscar_conta_por_cpf(cpf: str) -> int:
        """
        Busca o número da conta no arquivo contas.csv com base no CPF.
        
        :param cpf: O CPF do titular.
        :return: Número da conta associado ao CPF, ou None se não encontrado.
        """
        with open('contas.csv', mode='r', encoding='utf-8') as file_contas:
            reader = csv.reader(file_contas)
            for row in reader:
                if row[1] == cpf:  # O CPF está na segunda coluna (índice 1)
                    return int(row[0])  # Retorna o número da conta (primeira coluna)
        return None  # Retorna None caso o CPF não seja encontrado no arquivo contas
    

def buscar_numero_conta_por_cpf(cpf: str) -> int:
        """
        Busca o número da conta de um titular baseado no CPF.
        
        :param cpf: O CPF do titular.
        :return: Número da conta associado ao CPF, ou None se não encontrado.
        """
        # Primeiro, verifica se o CPF está no arquivo titulares.csv
        with open('titulares.csv', mode='r', encoding='utf-8') as file_titulares:
            reader = csv.reader(file_titulares)
            for row in reader:
                if row[2] == cpf:  # O CPF está na terceira coluna (índice 2)
                    # Se encontrou o CPF, busca o número da conta no arquivo contas.csv
                    return buscar_conta_por_cpf(cpf)
        return None  # Retorna None caso o CPF não seja encontrado no arquivo titulares