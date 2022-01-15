from fast_sql_manager.abstractions.repository import Repository
from fast_sql_manager.interfaces.db_config_interface import DBConfigInterface
import mysql.connector


class DataBaseConfig(DBConfigInterface):
  """ 
  Inicialização da classe de conexão
  ao banco
  """

  def __init__(self, host, port, user, password, db_name):
    self._host = host
    self._port = port
    self._user = user
    self._pass = password
    self._db = db_name
    self.name = db_name

  def get_connection(self):
    mydb = mysql.connector.connect(
      host=self._host,
      port=self._port,
      user=self._user,
      password=self._pass,
      database=self._db
    )
    return mydb


class MySQLRepository(Repository):
  def __init__(self, host: str, port, user: str, passwd: str, db_name: str = 'mysql'):
    super().__init__(db_config=DataBaseConfig(host, port, user, passwd, db_name))
