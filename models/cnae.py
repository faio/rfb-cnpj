from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String

Base = declarative_base()


class Cnae(Base):
    """
    Model com os dados do CNAE
    """
    __tablename__ = 'cnaes'

    # CÓDIGO DA ATIVIDADE ECONÔMICA
    codigo = Column(String, primary_key=True)

    # NOME DA ATIVIDADE ECONÔMICA
    descricao = Column(String)
