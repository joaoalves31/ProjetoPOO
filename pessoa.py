from validate_docbr import CPF

class Pessoa:
    proximo_id = 666  # Variável de classe para manter o próximo ID

    def __init__(self, nome: str = "", idade: int = 18, cpf: str = ""):
        self.__nome = nome 
        self.__idade = idade
        self.__cpf = cpf 
        self.__id = Pessoa.proximo_id  # Atribui o próximo ID disponível
        Pessoa.proximo_id += 1  # Incrementa o próximo ID para a próxima instância

    def get_id(self):
        return self.__id
    
        # Validações (se os valores forem fornecidos)
        '''if self.__nome and not self.__nome.isalpha():
            raise ValueError("O nome deve conter apenas letras.")
        if not (18 <= self.__idade <= 100):
            raise ValueError("A idade deve estar entre 18 e 100 anos.")
        if self.__cpf:
            validador_cpf = CPF()
            if not validador_cpf.validate(self.__cpf):
                raise ValueError("CPF inválido.")'''

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome: str = ""):
        if not nome.isalpha():
            raise ValueError("O nome deve conter apenas letras.")
        self.__nome = nome

    @property
    def idade(self):
        return self.__idade

    @idade.setter
    def idade(self, idade: int = 18):
        if not (18 <= idade  <= 100):
            raise ValueError("A idade deve estar entre 18 e 100 anos.")
        self.__idade = idade

    @property
    def cpf(self):
        return self.__cpf

    @cpf.setter
    def cpf(self, cpf: str = ""):
        validador_cpf = CPF()
        if not validador_cpf.validate(cpf):
            raise ValueError("CPF inválido.")
        self.__cpf = cpf

