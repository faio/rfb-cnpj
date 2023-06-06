from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Float, null, nulls_first

from rfb.models.natureza import Natureza
from rfb.models.qualificacao import Qualificacao

Base = declarative_base()


class Empresa(Base):
    __tablename__ = 'empresas'

    # NÚMERO BASE DE INSCRIÇÃO NO CNPJ (OITO PRIMEIROS DÍGITOS DO CNPJ).
    cnpj = Column(String(length=8), primary_key=True,  index=True)

    # NOME EMPRESARIAL DA PESSOA JURÍDICA
    razao = Column(String, index=True)

    # CÓDIGO DA NATUREZA JURÍDICA
    natureza = Column(Integer, index=True)

    # QUALIFICAÇÃO DA PESSOA FÍSICA RESPONSÁVEL PELA EMPRESA
    qualificacao_pf = Column(Integer, index=True)

    # CAPITAL SOCIAL DA EMPRESA
    capital = Column(Float, index=True)

    # CÓDIGO DO PORTE DA EMPRESA:
    # 1 – NÃO INFORMADO
    # 2 - MICRO EMPRESA
    # 03 - EMPRESA DE PEQUENO PORTE
    # 05 - DEMAIS
    porte = Column(Integer, index=True)

    # O ENTE FEDERATIVO RESPONSÁVEL É PREENCHIDO PARA OS CASOS
    # DE ÓRGÃOS E ENTIDADES DO GRUPO DE NATUREZA JURÍDICA 1XXX.
    # PARA AS DEMAIS NATUREZAS, ESTE ATRIBUTO FICA EM BRANCO.
    ente_federativo = Column(Integer, index=True)
