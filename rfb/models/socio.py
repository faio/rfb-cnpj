from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, String, Date, Integer

from rfb.models.empresa import Empresa
from rfb.models.pais import Pais
from rfb.models.qualificacao import Qualificacao

Base = declarative_base()


class Socio(Base):
    """
    Model com os dados do sócio
    """
    __tablename__ = 'socios'

    id = Column(Integer, primary_key=True, index=True)

    # NÚMERO BASE DE INSCRIÇÃO NO CNPJ (CADASTRO
    # NACIONAL DA PESSOA JURÍDICA).
    cnpj = Column(String(length=8),ForeignKey(Empresa.cnpj), index=True)

    # CÓDIGO DO IDENTIFICADOR DE SÓCIO
    # 1 – PESSOA JURÍDICA
    # 2 – PESSOA FÍSICA
    # 3 – ESTRANGEIRO
    identificador_socio = Column(Integer, index=True)

    # NOME DO SÓCIO PESSOA FÍSICA OU A RAZÃO SOCIAL E/OU NOME
    # EMPRESARIAL DA PESSOA JURÍDICA E/OU NOME DO
    # SÓCIO/RAZÃO SOCIAL DO SÓCIO ESTRANGEIRO
    nome = Column(String, index=True)

    # CPF OU CNPJ DO SÓCIO (SÓCIO ESTRANGEIRO NÃO TEM
    # ESTA INFORMAÇÃO).
    cpf_cnpj = Column(String(length=14), index=True)

    # CÓDIGO DA QUALIFICAÇÃO DO SÓCIO
    qualificacao = Column(Integer,ForeignKey(Qualificacao.codigo), index=True)

    # DATA DE ENTRADA NA SOCIEDADE
    data_entrada_sociedade = Column(Date)

    # CÓDIGO PAÍS DO SÓCIO ESTRANGEIRO
    codigo_pais = Column(Integer,ForeignKey(Pais.codigo), index=True)

    # NÚMERO DO CPF DO REPRESENTANTE LEGAL
    cpf_representante_legal = Column(String(length=11), index=True)

    # NOME DO REPRESENTANTE LEGAL
    nome_representante_legal = Column(String, index=True)

    # CÓDIGO DA QUALIFICAÇÃO DO REPRESENTANTE LEGAL
    qualificacao_representante_legal = Column(Integer,ForeignKey(Qualificacao.codigo), index=True)

    # CÓDIGO CORRESPONDENTE À FAIXA ETÁRIA DO SÓCIO
    faixa_etaria = Column(Integer, index=True)
