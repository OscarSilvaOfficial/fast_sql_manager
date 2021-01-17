import mysql.connector


class DataBase(object):
    """ 
      Inicialização da classe de conexão
      ao banco
    """

    def __init__(self, db_host, port, user, passwd, db_name):
        self._host = db_host
        self._port = port
        self._user = user
        self._pass = passwd
        self._db = db_name

    def getConnection(self):
        mydb = mysql.connector.connect(
            host=self._host,
            port=self._port,
            user=self._user,
            password=self._pass,
            database=self._db
        )
        return mydb


class Repository(object):
    """ 
      Os IFs iniciáis são checagens de tipo
      para que não seja possível a quebra das
      funções
    """

    def __init__(self, host: str, port, user: str, passwd: str, db_name: str = 'mysql'):
        self._db = DataBase(host, port, user, passwd, db_name)
        self._conn = self._db.getConnection()

    def createDataBase(self, db_name: str):
        """ 
          Para criar um Banco de Dados basta inserir o primeiro
          parâmetro `db_name` com o nome do Banco que deseja Criar

          EX: createDataBase('nome_do_banco')
        """

        if isinstance(db_name, str):
            cursor = self._conn.cursor()
            try:
                cursor.execute('CREATE DATABASE %s' % (db_name))
            except Exception as e:
                raise e
            return "Banco criado"
        else:
            raise 'db_name deve ser String'

    def createTable(self, tb_name: str, tb_columns: dict):
        """ 
          Para criar um tabela é necessário informar apenas o nome
          no parâmetro `tb_name` através  de uma String.

          Para informa como devem ser as colunas o parâmetro
          tb_coluns deve ser um dicionário, onde a chave seria o nome 
          da coluna e o valor os atributos da coluna

          EX: createTable('minha_tabela', {'id': 'int not null primary key auto_increment'})
        """

        if isinstance(tb_name, str) and isinstance(tb_columns, dict) == True:
            cursor = self._conn.cursor()

            re = []
            for col in zip(tb_columns.keys(), tb_columns.values()):
                re.append(' '.join(col))
            columns = ', '.join(re)

            sql = "CREATE TABLE `%s` (%s) " % (tb_name, columns)
            try:
                cursor.execute(sql)
            except Exception as e:
                raise e
            return 'Tabela criada'
        else:
            raise 'Tipos dos atributos não foram respeitados'

    def selectAll(self, tb_name: str):
        """ 
          Para selecionar todos os dados de uma tabela 
          é necessário apenas preencher através de uma
          string o parâmetro `tb_name` para informar 
          qual tabela você deseja puxar o dados

          EX: selectAll('nome_da_tabela') 
        """
        cursor = self._conn.cursor()

        if isinstance(tb_name, str):
            try:
                cursor.execute('SELECT * FROM `%s`' % (tb_name))
            except Exception as e:
                raise e

            re = []
            for data in cursor.fetchall():
                re.append(data)

            return re
        else:
            raise "Tipo da variável tb_name dever ser String"

    def insert(self, tb_name: str, tb_columns: list, insert_values: tuple):
        """ 
        Para inserir os dados em uma tabela é necessário informar o nome da tabela
        no `tb_name` como String, as colunas de deseja inserir no `tb_columns`
        como um Lista e os valores que deseja inserir `insert_values` como uma tupla

        EX: inser(table_name='pessoas', tb_columns=['cpf', 'nome', 'idade'], insert_values=('000000000', 'João', 19))
        """
        cursor = self._conn.cursor()

        if isinstance(tb_name, str) and isinstance(tb_columns, list) and isinstance(insert_values, tuple):
            columns = ', '.join(tb_columns)
            values = str(insert_values).replace('(', '').replace(')', '')
            sql = "INSERT INTO %s (%s) VALUES (%s)" % (
                tb_name, columns, values)

            try:
                cursor.execute(sql)
                self._conn.commit()
            except Exception as e:
                raise e
            return '{0} linha(s) afetadas'.format(cursor.rowcount)
        else:
            raise 'Tipos dos atributos não foram respeitados'

    def update(self, tb_name: str, set: dict, where: dict):
        """ 
          Para realizar o update informe o parâmetro tb_name como String.
          O parâmetro `set` deve ser um Dicionário, sendo a chave a coluna que deseja alterar,
          e o valor sendo o novo valor dessa coluna.
          O parâmetro where também é um Dicionário contendo seu primeiro par de chave e valor com a coluna que deseja
          realizar o filtro where e o valor que a coluna deve conter

          EX: update('tab_pessoa', {'nome': 'Joãozinho', 'idade': 17}, {'cpf': '123456789'})

          É possível também inserir dentro do where operadores condicionáis, porém o parametro muda um pouco
          pois é necessário dentro do dicionário informar qual a condicional que deseja usar

          EX: update(
            tb_name='tab_pessoa',
            set={'nome': 'Joãozinho', 'idade': 17},
            where={
              'cpf': {'value':'123456789', 'condicional': 'and'}, 
              'name': 'João',
              }
          )
        """
        cursor = self._conn.cursor()

        set_re = []
        for set in zip(set.keys(), set.values()):
            re = "{0}='{1}'".format(set[0], set[1])
            set_re.append(re)
        set = ', '.join(set_re)

        where_re = []

        for key, data in where.items():

            if 'condicional' in data:
                if data['condicional'] == 'or' or data['condicional'] == 'OR':
                    re = "{0}='{1}' OR".format(key, data['value'])
                    where_re.append(re)
                if data['condicional'] == 'and' or data['condicional'] == 'AND':
                    re = "{0}='{1}' AND".format(key, data['value'])
                    where_re.append(re)
            else:
                if 'value' in data:
                    re = "{0}='{1}'".format(key, data['value'])
                else:
                    re = "{0}='{1}'".format(key, data)
                where_re.append(re)

        where_re = ' '.join(where_re)
        sql = "UPDATE %s SET %s WHERE (%s)" % (tb_name, set, where_re)

        try:
            cursor.execute(sql)
            self._conn.commit()
        except Exception as e:
            raise e
        return '{0} linha(s) afetadas'.format(cursor.rowcount)

    def delete(self, tb_name: str, where: dict):
        """ 
          Para realizar o update informe o parâmetro `tb_name` como String.

          O parâmetro where também é um Dicionário contendo seu primeiro par de chave e valor com a coluna que deseja
          realizar o filtro where e o valor que a coluna deve conter

          EX: delete('tab_pessoa', {'cpf': '123456789'})

          É possível também inserir dentro do where operadores condicionáis, porém o parametro muda um pouco
          pois é necessário dentro do dicionário informar qual a condicional que deseja usar

          EX: delete(
            tb_name='tab_pessoa',
            where={
              'cpf': {'value':'123456789', 'condicional': 'and'}, 
              'name': 'João',
              }
          )
        """
        cursor = self._conn.cursor()

        where_re = []
        for key, data in where.items():

            if 'condicional' in data:
                if data['condicional'] == 'or' or data['condicional'] == 'OR':
                    re = "{0}='{1}' OR".format(key, data['value'])
                    where_re.append(re)
                if data['condicional'] == 'and' or data['condicional'] == 'AND':
                    re = "{0}='{1}' AND".format(key, data['value'])
                    where_re.append(re)
            else:
                re = "{0}='{1}'".format(key, data)
                where_re.append(re)

        where_re = ' '.join(where_re)
        sql = "DELETE FROM %s WHERE (%s)" % (tb_name, where_re)

        try:
            cursor.execute(sql)
            self._conn.commit()
        except Exception as e:
            raise e
        return '{0} linha(s) afetadas'.format(cursor.rowcount)