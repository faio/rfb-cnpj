from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer

Base = declarative_base()


class Pais(Base):
    __tablename__ = 'paises'

    # CÓDIGO DO PAÍS
    codigo = Column(Integer, primary_key=True)

    # NOME DO PAÍS
    descricao = Column(String)
