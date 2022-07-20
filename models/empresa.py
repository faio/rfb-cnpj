from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Float

Base = declarative_base()


class Empresa(Base):
    __tablename__ = 'empresas'

    id = Column(Integer, primary_key=True)

    # NÚMERO BASE DE INSCRIÇÃO NO CNPJ (OITO PRIMEIROS DÍGITOS DO CNPJ).
    cnpj = Column(String(length=8))

    # NOME EMPRESARIAL DA PESSOA JURÍDICA
    razao = Column(String)

    # CÓDIGO DA NATUREZA JURÍDICA
    natureza = Column(Integer)

    # QUALIFICAÇÃO DA PESSOA FÍSICA RESPONSÁVEL PELA EMPRESA
    qualificacao_pf = Column(Integer)

    # CAPITAL SOCIAL DA EMPRESA
    capital = Column(Float)

    # CÓDIGO DO PORTE DA EMPRESA:
    # 1 – NÃO INFORMADO
    # 2 - MICRO EMPRESA
    # 03 - EMPRESA DE PEQUENO PORTE
    # 05 - DEMAIS
    porte = Column(Integer)

    # O ENTE FEDERATIVO RESPONSÁVEL É PREENCHIDO PARA OS CASOS
    # DE ÓRGÃOS E ENTIDADES DO GRUPO DE NATUREZA JURÍDICA 1XXX.
    # PARA AS DEMAIS NATUREZAS, ESTE ATRIBUTO FICA EM BRANCO.
    ente_federativo = Column(Integer)
