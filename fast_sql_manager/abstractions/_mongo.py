from fast_sql_manager.interfaces.db_config_interface import DBConfigInterface
from pymongo import MongoClient

class Mongo(object):
  """ 
    Os IFs iniciáis são checagens de tipo
    para que não seja possível a quebra das
    funções
  """

  def __init__(self, db_config: DBConfigInterface, db_name: str = 'mongo'):
    self._conn: MongoClient = db_config.get_connection()
    self._db_name = db_name
      
  def select_all(self, collection_name, where={}, return_data=[]):
    collection = self._conn[self._db_name][collection_name]
    for item in collection.find(where): return_data.append(item)
    return return_data