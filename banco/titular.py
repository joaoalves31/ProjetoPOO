from pessoa import Pessoa

class Titular(Pessoa):
    def __init__(self, nome: str, cpf: str, idade: int, login: str, senha:str):
        super().__init__(nome, cpf, idade)
        self.login = login
        self.senha = senha

    def autenticar(self, login: str, senha: str):
        pass