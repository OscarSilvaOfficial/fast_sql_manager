from fast_sql_manager.implementations.sqlite import SQLiteRepository

db = SQLiteRepository(db_path='teste.db')

def create_tables():
  db.create_table(
    name='tb_teste',
    columns={
      'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
      'name': 'varchar(255)',
    }
  )
  db.insert(
    table_name='tb_teste',
    table_columns=['name'],
    insert_values=('Oscar',)
  )


def test_select():
  create_tables()
  print("Regístros adicionados: ", len(db.select_all('tb_teste')))
  