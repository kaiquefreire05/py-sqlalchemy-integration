from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import func
from sqlalchemy import inspect
from sqlalchemy import create_engine
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import select

Base = declarative_base()


class User(Base):
    __tablename__ = "user_account"  # Declarando o nome da tabela

    # atributos

    id = Column(Integer, primary_key=True)  # Definindo o ID como primary key
    name = Column(String)
    fullname = Column(String)

    address = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"

        # cascade="all, delete-orphan", qualquer ligação com Address será apagado evitando repetição e classes soltas
        # Define como a relação será vista do lado do modelo

    )

    def __repr__(self):  # Construtor
        return f"user(id={self.id}, name={self.name}, fullname={self.fullname})"


class Address(Base):
    __tablename__ = "address"  # Declarando nome da tabela

    id = Column(Integer, primary_key=True)
    # O tamanho da String vai ser de 40 caracteres
    email_address = Column(String(40), nullable=False)  # O atributo email_email_address não pode ser vazio ou null
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)  # Chave estrangeira que faz a ref a id

    user = relationship("User", back_populates="address")

    def __repr__(self):  # Construtor
        return f"Address (id={self.id}, email_address={self.email_address})"  # Não precisa inserir a chave estrangeira


# Conexão com o DataBase

engine = create_engine("sqlite://")

# Criando as classes como tabela no banco de dados

Base.metadata.create_all(engine)

# Investiga o esquema do banco de dados

inspetor_engine = inspect(engine)
print(inspetor_engine.has_table("user_account"))  # Retornando True
print(inspetor_engine.get_table_names())  # Vendo os nomes das tabelas criadas
print(inspetor_engine.default_schema_name)

# With, inicia uma sessão com o banco de dados especificado pelo engine, ela garante que a sessão é fechada corretamente
with Session(engine) as session:
    kaique = User(  # Variável do tipo User e também vai ter a estrutura de address
        name='Kaique',
        fullname='Kaique Freire',
        address=[Address(email_address='kaiquefreire@gmail.com')]
    )

    maria = User(
        name='Maria',
        fullname='Maria Teresa',
        address=[Address(email_address='maria@gamail.com'),  # Forma de adicionar 2 emails diferentes, DB RELACIONAL!!!
                 Address(email_address='mariasecundario@gmail.org')]
    )

    victor = User(
        name='Victor', fullname='Victor Peixoto'
    )

    # Enviado para o DataBase (persistência de dados)
    session.add_all([kaique, maria, victor])

    session.commit()  # Marca o fim da transação e envia para o DB

print('Recuperando usuários a partir de condição de filtragem')
stmt = select(User).where(User.name.in_(['Kaique', 'Victor']))  # Selecione User Onde Name == 'Kaique'
for user in session.scalars(stmt):
    print(user)


print('\nRecuperando endereços email de Maria')
stmt_address = select(Address).where(Address.user_id.in_([2]))  # user_id é referente ao id da classe User
for address in session.scalars(stmt_address):
    print(address)

print('\nRecuperando info de maneira ordenada')
print('Forma crescente que vem por padrão')
stmt_order_cresc = select(User).order_by(User.fullname)
for result in session.scalars(stmt_order_cresc):
    print(result)

print('\nForma decrescente')
stmt_order_decr = select(User).order_by(User.fullname.desc())
for result in session.scalars(stmt_order_decr):
    print(result)

print()
stmt_join = select(User.fullname, Address.email_address).join_from(Address, User)
for result in session.scalars(stmt_join):  # Scalars pega somente o resultado, por isso não voltou o email
    print(result)
print(select(User.fullname, Address.email_address).join_from(Address, User))

print('\nExecutando statement a partir da connection')
connection = engine.connect()
results = connection.execute(stmt_join).fetchall()  # Retornar tudo
for res in results:
    print(res)

print('\nTotal de instâncias em User:')
stmt_count = select(func.count('*')).select_from(User)
for result in session.scalars(stmt_count):  # Scalars pega somente o resultado, por isso não voltou o email
    print(result)
