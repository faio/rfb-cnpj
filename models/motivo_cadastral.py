from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer

Base = declarative_base()


class MotivoCadastral(Base):
    __tablename__ = 'motivo_cadastral'

    # CÓDIGO DO MOTIVO CADASTRAL
    codigo = Column(Integer, primary_key=True)

    # NOME DO MOTIVO CADASTRAL
    descricao = Column(String)
