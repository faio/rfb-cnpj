from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String

Base = declarative_base()


class Pais(Base):
    __tablename__ = 'pais'

    # CÓDIGO DO PAÍS
    codigo = Column(String, primary_key=True)

    # NOME DO PAÍS
    descricao = Column(String)
