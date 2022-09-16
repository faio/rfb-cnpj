from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, String, Integer

Base = declarative_base()


class Cidade(Base):
    """
    Model com os dados da cidade
    """
    __tablename__ = 'cidades'

    # NOME DA CIDADE
    nome = Column(String)

    # UF
    uf = Column(String(length=2))

    # ibge
    ibge = Column(Integer)

    # latitude
    latitude = Column(Float)

    # longitude
    longitude = Column(Float)

    # cod_tom
    cod_tom = Column(Integer, primary_key=True)
