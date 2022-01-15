# Introdução

Essa biblioteca foi criada como uma forma de abstração das operações mais simples
de um banco de dados MySQL.

# Início

Após fazer a instalação com o pip install fast_sql_manager
é necessário que você importe a classe correspondente ao banco
que deseja manipular.

```python
from fast_sql_manager.implementations.mysql import MySQLRepository
```
ou
```python
from fast_sql_manager.implementations.sqlite import SQLiteRepository
```

Ao importar a classe você pode instância-la ou
usa-la diretamente preenchendo os parâmetros necessários.

```python
db = Repository(
    host='localhost', 
    port=3307, 
    user='root', 
    passwd='root', 
    db_name='sys'
)
```

# Métodos 

## createDataBase

Para criar um Banco de Dados basta inserir o primeiro
parâmetro `db_name` com o nome do Banco que deseja Criar.

```python
db.create_database('nome_do_banco')
```

## createTable

Para criar um tabela é necessário informar apenas o nome
no parâmetro `name` através  de uma String.

Para informar como devem ser as colunas o parâmetro
`coluns` deve ser um dicionário, onde a chave seria o nome 
da coluna e o valor os atributos da coluna.

```python
db.create_table(
    name='minha_tabela', 
    columns={'id': 'int not null primary key auto_increment'}
)
```

## selectAll

Para selecionar todos os dados de uma tabela 
é necessário apenas preencher através de uma
string o parâmetro `table_name` para informar 
qual tabela você deseja puxar o dados

```python
db.select_all(table_name='nome_da_tabela') 
```

## insert

Para inserir os dados em uma tabela é necessário informar o nome da tabela no `table_name` como String, as colunas de deseja inserir no `table_columns` como uma Lista e os valores que deseja inserir no `insert_values` como uma Tupla.

```python
db.insert(
    table_name='pessoas',
    tb_columns=['cpf', 'nome', 'idade'], 
    insert_values=('000000000', 'João', 19)
)
```

## update

Para realizar o update informe o parâmetro tb_name como String.
O parâmetro `set` deve ser um Dicionário, sendo a chave a coluna que deseja alterar,
e o valor sendo o novo valor dessa coluna.
O parâmetro `where` também é um Dicionário contendo seu primeiro par de chave e valor com a coluna que deseja
realizar o filtro where e o valor que a coluna deve conter.

```python
db.update(
    table_name='tab_pessoa',
    set={'nome': 'Joãozinho', 'idade': 17},
    where={'cpf': '123456789'}
)
```

É possível também inserir dentro do `where` operadores condicionais, porém o parametro muda um pouco
pois é necessário dentro do dicionário informar qual a condicional que deseja usar.

```python
db.update(
    tb_name='tab_pessoa',
    set={'nome': 'Joãozinho', 'idade': 17},
    where={
        'cpf': {'value':'123456789', 'condicional': 'and'}, 
        'name': 'João',
    }
)
```

## delete

Para realizar o update informe o parâmetro `tb_name` como String.

O parâmetro where também é um Dicionário contendo seu primeiro par de chave e valor com a coluna que deseja
realizar o filtro where e o valor que a coluna deve conter.

```python
    db.delete('tab_pessoa', {'cpf': '123456789'})
```

É possível também inserir dentro do where operadores condicionais, porém o parâmetro muda um pouco
pois é necessário dentro do dicionário informar qual a condicional que deseja usar.

```python
db.delete(
    tb_name='tab_pessoa',
    where={
        'cpf': {'value':'123456789', 'condicional': 'and'}, 
        'name': 'João',
        }
)
```