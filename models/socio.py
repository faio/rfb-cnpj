from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Date, Integer

Base = declarative_base()


class Socio(Base):
    """
    Model com os dados do sócio
    """
    __tablename__ = 'socios'

    id = Column(Integer, primary_key=True)

    # NÚMERO BASE DE INSCRIÇÃO NO CNPJ (CADASTRO
    # NACIONAL DA PESSOA JURÍDICA).
    cnpj = Column(String(length=8))

    # CÓDIGO DO IDENTIFICADOR DE SÓCIO
    # 1 – PESSOA JURÍDICA
    # 2 – PESSOA FÍSICA
    # 3 – ESTRANGEIRO
    identificador_socio = Column(Integer)

    # NOME DO SÓCIO PESSOA FÍSICA OU A RAZÃO SOCIAL E/OU NOME
    # EMPRESARIAL DA PESSOA JURÍDICA E/OU NOME DO
    # SÓCIO/RAZÃO SOCIAL DO SÓCIO ESTRANGEIRO
    nome = Column(String)

    # CPF OU CNPJ DO SÓCIO (SÓCIO ESTRANGEIRO NÃO TEM
    # ESTA INFORMAÇÃO).
    cpf_cnpj = Column(String(length=14))

    # CÓDIGO DA QUALIFICAÇÃO DO SÓCIO
    qualificacao = Column(Integer)

    # DATA DE ENTRADA NA SOCIEDADE
    data_entrada_sociedade = Column(Date)

    # CÓDIGO PAÍS DO SÓCIO ESTRANGEIRO
    codigo_pais = Column(Integer)

    # NÚMERO DO CPF DO REPRESENTANTE LEGAL
    cpf_representante_legal = Column(String(length=11))

    # NOME DO REPRESENTANTE LEGAL
    nome_representante_legal = Column(String)

    # CÓDIGO DA QUALIFICAÇÃO DO REPRESENTANTE LEGAL
    qualificacao_representante_legal = Column(Integer)

    # CÓDIGO CORRESPONDENTE À FAIXA ETÁRIA DO SÓCIO
    faixa_etaria = Column(Integer)
