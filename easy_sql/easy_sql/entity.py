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