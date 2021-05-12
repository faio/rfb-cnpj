from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer

Base = declarative_base()


class Municipio(Base):
    __tablename__ = 'municipios'

    # CÓDIGO DO MUNICÍPIO
    codigo = Column(Integer, primary_key=True)

    # NOME DO MUNICÍPIO
    descricao = Column(String)
