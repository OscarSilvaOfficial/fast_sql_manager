from .implementations.mongo import MongoRepository

mongo = MongoRepository(
  db_str_connection='mongodb://localhost:27017/',
  db_name='local'
) 

def test_mongo():
  assert type(mongo.select_all(collection_name='startup_log')) == list