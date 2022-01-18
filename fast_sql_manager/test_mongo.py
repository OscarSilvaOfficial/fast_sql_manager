from .implementations.mongo import MongoRepository

mongo = MongoRepository(
  db_str_connection='mongodb://localhost:27017/',
  db_name='local'
) 

def test_mongo():
  mongo.create_collection('teste')
  mongo.create_document('teste', {'name': 'Oscar'})
  response = mongo.select_all(collection_name='teste')
  mongo.delete_collection('teste')
  print(response)
  assert type(response) == list