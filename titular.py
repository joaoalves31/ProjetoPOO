from pessoa import Pessoa
import re
import hashlib
from gerencia_banco_dados import gerencia_banco_dados

class Titular(Pessoa):
    def __init__(self, nome: str, idade: int, cpf: str, login: str = "", senha: str = ""):
        super().__init__(nome, idade, cpf)

        self.__login = login
        self.__senha = self.hash_senha(senha)

    @staticmethod
    def hash_senha(senha: str) -> str:
        return hashlib.sha256(senha.encode()).hexdigest()
    
    @staticmethod
    def validar_senha(senha: str) -> bool:
    # Verifica se a senha tem pelo menos 8 caracteres e contém letras minúsculas e números
        if len(senha) < 8:
            return False
        if not re.search(r"[a-z]", senha):  # Verifica se há pelo menos uma letra minúscula
            return False
        if not re.search(r"[0-9]", senha):  # Verifica se há pelo menos um número
            return False
        return True

    def get_senha(self):
        return self.__senha
    
    def get_login(self):
        return self.__login
    
    def get_id(self):
        return self._Pessoa__id  # Acessa o ID da classe Pai (Pessoa)
    
    def salvar_no_banco(self):
        if not self.db: raise ValueError("Banco de dados não configurado.")

        # Inserir dados na tabela "pessoas"
        comando_pessoa = "INSERT INTO pessoas (nome, idade, cpf) VALUES (%s, %s, %s)"
        parametros_pessoa = (self.nome, self.idade, self.cpf)
        self.db.executar_comando(comando_pessoa, parametros_pessoa)

        # Recuperar o ID gerado para a pessoa inserida
        comando_ultimo_id = "SELECT LAST_INSERT_ID()"
        pessoa_id_resultado = self.db.consultar_dados(comando_ultimo_id)
        pessoa_id = pessoa_id_resultado[0]["LAST_INSERT_ID()"]

        # Inserir dados na tabela "titulares"
        comando_titular = "INSERT INTO titulares (login, senha, pessoa_id) VALUES (%s, %s, %s)"
        parametros_titular = (self.__login, self.__senha, pessoa_id)
        self.db.executar_comando(comando_titular, parametros_titular)

        # Recuperar o ID gerado para o titular inserido
        comando_ultimo_id_titular = "SELECT LAST_INSERT_ID()"
        titular_id_resultado = self.db.consultar_dados(comando_ultimo_id_titular)
        self.__id = titular_id_resultado[0]["LAST_INSERT_ID()"]

    def atualizar_no_banco(self):
        if not self.db: raise ValueError("Banco de dados não configurado.")

        # Atualizar dados do titular na tabela "titulares"
        colunas_valores = {"login": self.__login, "senha": self.__senha}
        condicao = f"pessoa_id = (SELECT id FROM pessoas WHERE cpf = '{self.cpf}')"
        self.db.atualizar_registro("titulares", colunas_valores, condicao)

        # Commit já realizado pela classe gerenciadora, então não é necessário chamar novamente
        print(f"Titular {self.__login} atualizado no banco de dados.")