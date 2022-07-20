from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer

Base = declarative_base()


class Qualificacao(Base):
    __tablename__ = 'qualificacoes'

    # CÓDIGO DA QUALIFICAÇÃO DO SÓCIO
    codigo = Column(Integer, primary_key=True)

    # NOME DA QUALIFICAÇÃO DO SÓCIO
    descricao = Column(String)
