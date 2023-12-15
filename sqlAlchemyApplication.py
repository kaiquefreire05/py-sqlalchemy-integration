from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import inspect
from sqlalchemy import create_engine
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

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
        return f"Address (id={self.id}, email={self.email_address})"  # Não precisa inserir a chave estrangeira


# Conexão com o DataBase

engine = create_engine("sqlite://")

# Criando as classes como tabela no banco de dados

Base.metadata.create_all(engine)

# Investiga o esquema do banco de dados

inspetor_engine = inspect(engine)
print(inspetor_engine.has_table("user_account"))  # Retornando True
print(inspetor_engine.get_table_names())  # Vendo os nomes das tabelas criadas
print(inspetor_engine.default_schema_name)
