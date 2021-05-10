from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String

Base = declarative_base()


class Municipio(Base):
    __tablename__ = 'municipio'

    # CÓDIGO DO MUNICÍPIO
    codigo = Column(String, primary_key=True)

    # NOME DO MUNICÍPIO
    descricao = Column(String)
