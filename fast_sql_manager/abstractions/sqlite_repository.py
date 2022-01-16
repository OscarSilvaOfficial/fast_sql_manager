from http.client import ImproperConnectionState
from sqlite3 import OperationalError
from fast_sql_manager.interfaces.db_config_interface import DBConfigInterface

class SQLiteRepository(object):
    """ 
      Os IFs iniciáis são checagens de tipo
      para que não seja possível a quebra das
      funções
    """

    def __init__(self, db_config: DBConfigInterface):
        self._conn = db_config.get_connection()
        
    def create_table(self, name: str, columns: dict):
        """ 
          Para criar um tabela é necessário informar apenas o nome
          no parâmetro `table_name` através  de uma String.

          Para informa como devem ser as colunas o parâmetro
          table_coluns deve ser um dicionário, onde a chave seria o nome 
          da coluna e o valor os atributos da coluna

          EX: create_table('minha_tabela', {'id': 'int not null primary key auto_increment'})
        """

        if isinstance(name, str) and isinstance(columns, dict) == True:
            cursor = self._conn.cursor()

            re = []
            
            for col in zip(columns.keys(), columns.values()):
                column_name = "`%s`" % col[0] 
                column_type = col[1]
                field = (column_name, column_type)
                re.append(' '.join(field))
                
            columns = ', '.join(re)

            sql = "CREATE TABLE %s (%s)" % (name, columns) 
            
            try:
                cursor.execute(sql)
            except OperationalError as e:
                return 'Tabela criada'
            except Exception as e:
                raise e
            return 'Tabela criada'
        else:
            raise 'Tipos dos atributos não foram respeitados'

    def select_all(self, table_name: str, where: dict = {}):
        """ 
          Para selecionar todos os dados de uma tabela 
          é necessário apenas preencher através de uma
          string o parâmetro `table_name` para informar 
          qual tabela você deseja puxar o dados

          EX: select_all('nome_da_tabela') 
        """
        cursor = self._conn.cursor()

        if isinstance(table_name, str):
            if where == {}:
                try:
                    cursor.execute('SELECT * FROM %s' % (table_name))
                except Exception as e:
                    raise e
            else:
                try:
                    where_re = []
                    for key, data in where.items():

                        if 'condicional' in str(data):
                            if data['condicional'] == 'or' or data['condicional'] == 'OR':
                                re = "{0}='{1}' OR".format(key, data['value'])
                                where_re.append(re)
                            if data['condicional'] == 'and' or data['condicional'] == 'AND':
                                re = "{0}='{1}' AND".format(key, data['value'])
                                where_re.append(re)
                        else:
                            if 'value' in str(data):
                                re = "{0}='{1}'".format(key, data['value'])
                            else:
                                re = "{0}='{1}'".format(key, data)
                            where_re.append(re)

                    where_re = ' '.join(where_re)
                    cursor.execute('SELECT * FROM %s WHERE (%s)' % (table_name, where_re))
                except Exception as e:
                    raise e

            response = []
            for data in cursor.fetchall():
                row = {}
                for index, column_name in enumerate(list(map(lambda x: x[0], cursor.description))):
                    row[column_name] = data[index]
                response.append(row)

            return response if len(response) > 1 else response[0]
        else:
            raise "Tipo da variável table_name dever ser String"

    def insert(self, table_name: str, table_columns: list, insert_values: tuple):
        """ 
        Para inserir os dados em uma tabela é necessário informar o nome da tabela
        no `table_name` como String, as colunas de deseja inserir no `table_columns`
        como um Lista e os valores que deseja inserir `insert_values` como uma tupla

        EX: inser(table_name='pessoas', table_columns=['cpf', 'nome', 'idade'], insert_values=('000000000', 'João', 19))
        """
        cursor = self._conn.cursor()

        if isinstance(table_name, str) and isinstance(table_columns, list) and isinstance(insert_values, tuple):
            columns = ', '.join(table_columns)
            values = str(insert_values).replace('(', '').replace(')', '') if len(insert_values) > 1 else f"'{insert_values[0]}'"
            sql = "INSERT INTO %s (%s) VALUES (%s)" % (table_name, columns, values)

            try:
                cursor.execute(sql)
                self._conn.commit()
            except Exception as e:
                raise e
            
            return '{0} linha(s) afetadas'.format(cursor.rowcount)
        else:
            raise 'Tipos dos atributos não foram respeitados'

    def update(self, table_name: str, set: dict, where: dict):
        """ 
          Para realizar o update informe o parâmetro table_name como String.
          O parâmetro `set` deve ser um Dicionário, sendo a chave a coluna que deseja alterar,
          e o valor sendo o novo valor dessa coluna.
          O parâmetro where também é um Dicionário contendo seu primeiro par de chave e valor com a coluna que deseja
          realizar o filtro where e o valor que a coluna deve conter

          EX: update('tab_pessoa', {'nome': 'Joãozinho', 'idade': 17}, {'cpf': '123456789'})

          É possível também inserir dentro do where operadores condicionáis, porém o parametro muda um pouco
          pois é necessário dentro do dicionário informar qual a condicional que deseja usar

          EX: update(
            table_name='tab_pessoa',
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

            if 'condicional' in str(data):
                if data['condicional'] == 'or' or data['condicional'] == 'OR':
                    re = "{0}='{1}' OR".format(key, data['value'])
                    where_re.append(re)
                if data['condicional'] == 'and' or data['condicional'] == 'AND':
                    re = "{0}='{1}' AND".format(key, data['value'])
                    where_re.append(re)
            else:
                if 'value' in str(data):
                    re = "{0}='{1}'".format(key, data['value'])
                else:
                    re = "{0}='{1}'".format(key, data)
                where_re.append(re)

        where_re = ' '.join(where_re)
        sql = "UPDATE %s SET %s WHERE (%s)" % (table_name, set, where_re)

        try:
            cursor.execute(sql)
            self._conn.commit()
        except Exception as e:
            raise e
        return '{0} linha(s) afetadas'.format(cursor.rowcount)

    def delete(self, table_name: str, where: dict):
        """ 
          Para realizar o update informe o parâmetro `table_name` como String.

          O parâmetro where também é um Dicionário contendo seu primeiro par de chave e valor com a coluna que deseja
          realizar o filtro where e o valor que a coluna deve conter

          EX: delete('tab_pessoa', {'cpf': '123456789'})

          É possível também inserir dentro do where operadores condicionáis, porém o parametro muda um pouco
          pois é necessário dentro do dicionário informar qual a condicional que deseja usar

          EX: delete(
            table_name='tab_pessoa',
            where={
              'cpf': {'value':'123456789', 'condicional': 'and'}, 
              'name': 'João',
              }
          )
        """
        cursor = self._conn.cursor()

        where_re = []
        for key, data in where.items():

            if 'condicional' in str(data):
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
        sql = "DELETE FROM %s WHERE (%s)" % (table_name, where_re)

        try:
            cursor.execute(sql)
            self._conn.commit()
        except Exception as e:
            raise e
        return '{0} linha(s) afetadas'.format(cursor.rowcount)