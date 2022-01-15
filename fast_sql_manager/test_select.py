from repository import Repository

db = Repository(
  host='localhost',
  port=3306, 
  user='root', 
  passwd='admin',
)

def create_tables():
  db.create_database('teste')
  db.create_table(
    name='tb_teste',
    columns={
      'id': 'int not null primary key auto_increment',
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
  print(db.select_all('tb_teste'))
  
test_select()