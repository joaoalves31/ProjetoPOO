import hashlib
from pessoa import Pessoa

class Titular(Pessoa):
    def __init__(self, nome, idade, cpf, login, senha):
        super().__init__(nome, idade, cpf)
        self.__login = login
        self.__senha = senha #hashlib.sha256(senha.encode()).hexdigest()

    @property
    def login(self):
        return self.__login
    
    @login.setter
    def login(self, login):
        self.__login = login

    @property
    def senha(self):
        return self.__senha
    
    @senha.setter
    def senha(self, senha):
        self.__senha = senha #hashlib.sha256(senha.encode()).hexdigest()