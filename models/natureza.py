from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer

Base = declarative_base()


class Natureza(Base):
    __tablename__ = 'naturezas'

    # CÓDIGO DA NATUREZA JURÍDICA
    codigo = Column(Integer, primary_key=True)

    # NOME DA NATUREZA JURÍDICA
    descricao = Column(String)
