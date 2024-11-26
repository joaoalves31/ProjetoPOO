import mysql.connector
from mysql.connector import Error
class gerencia_banco_dados:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conexao = None

    def conectar(self):
        """Estabelece a conexão com o banco de dados."""
        try:
            self.conexao = mysql.connector.connect(
                host='localhost',
                user='usuario_trabalho',
                password='senha_segura',
                database='banco_trabalho'
            )
            if self.conexao.is_connected():
                print("Conexão estabelecida com sucesso.")
        except Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            self.conexao = None

    def desconectar(self):
        """Fecha a conexão com o banco de dados."""
        if self.conexao and self.conexao.is_connected():
            self.conexao.close()
            print("Conexão fechada.")

    def executar_comando(self, comando, parametros=None):
        """Executa um comando SQL no banco de dados."""
        if not self.conexao or not self.conexao.is_connected():
            print("Conexão não estabelecida. Use o método 'conectar' primeiro.")
            return
        try:
            cursor = self.conexao.cursor()
            cursor.execute(comando, parametros)
            self.conexao.commit()
            print("Comando executado com sucesso.")
        except Error as e:
            print(f"Erro ao executar o comando: {e}")

    def consultar_dados(self, comando, parametros=None):
        """Consulta dados no banco de dados e retorna os resultados."""
        if not self.conexao or not self.conexao.is_connected():
            print("Conexão não estabelecida. Use o método 'conectar' primeiro.")
            return []
        try:
            cursor = self.conexao.cursor(dictionary=True)
            cursor.execute(comando, parametros)
            return cursor.fetchall()
        except Error as e:
            print(f"Erro ao consultar dados: {e}")
            return []

    def atualizar_registro(self, tabela, colunas_valores, condicao):
        """Atualiza registros no banco de dados."""
        if not self.conexao or not self.conexao.is_connected():
            print("Conexão não estabelecida. Use o método 'conectar' primeiro.")
            return

        colunas = ", ".join([f"{coluna} = %s" for coluna in colunas_valores.keys()])
        valores = list(colunas_valores.values())

        query = f"UPDATE {tabela} SET {colunas} WHERE {condicao};"
        try:
            cursor = self.conexao.cursor()
            cursor.execute(query, valores)
            self.conexao.commit()
            print("Registro atualizado com sucesso.")
        except Error as e:
            print(f"Erro ao atualizar registro: {e}")
