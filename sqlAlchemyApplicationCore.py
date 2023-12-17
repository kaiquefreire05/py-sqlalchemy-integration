from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, text

engine = create_engine("sqlite:///:memory:?memory=True", echo=False)
# echo=True, mostra os comandos sql
# echo=False, somente cria e não mostra os comandos

metadata_obj = MetaData()  # Definindo o nome do schema

user = Table(
    'user',  # Nome da tabela
    metadata_obj,  # Variável do schema
    Column('user_id', Integer, primary_key=True),  # Atributos
    Column('user_name', String(60), nullable=False),
    Column('email', String(60)),
    Column('nickname', String(40), nullable=False)

)

user_prefs = Table(
    'user_prefs',  # Nome da tabela
    metadata_obj,  # Variável do schema
    Column('pref_id', Integer, primary_key=True),  # Atributos
    Column('user_id', Integer, ForeignKey('user.user_id'), nullable=False),  # Define quem está sendo referenciado
    Column('pref_name', String(60), nullable=False),
    Column('pref_value', String(100)),


)

for table in metadata_obj.sorted_tables:  # Dando print nos nomes das tabelas que existe no schema
    print(table)

print('Info da tabela user')
print(user_prefs.primary_key)
print(user_prefs.constraints)

metadata_obj.create_all(engine)

# Criando um segundo banco de dados

metadata_db_obj = MetaData(schema='bank')

financial_info = Table(
    'financial_info',  # Nome da tabela
    metadata_db_obj,  # Variável do schema
    Column('id', Integer, primary_key=True),  # Atributos
    Column('value', String(100), nullable=False)

)

# Inserindo info na tabela user
sql_insert = text("insert into user values(1,'Kaique','kaique@email.com','freire')")
engine.execute(sql_insert)

print('\nInfo da tabela financial_info')
print(financial_info.primary_key)
print(financial_info.constraints)


print('\nExecutando statement sql')
sql = text('select * from user')
result = engine.execute(sql)

for row in result:
    print(row)






