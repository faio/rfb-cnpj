from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Date, Integer

Base = declarative_base()


class DadoSimples(Base):
    """
    Model com os dados do simples nacional
    """
    __tablename__ = 'dados_simples'

    id = Column(Integer, primary_key=True)

    # NÚMERO BASE DE INSCRIÇÃO NO CNPJ (OITO PRIMEIROS
    # DÍGITOS DO CNPJ).
    cnpj = Column(String(length=8))

    # INDICADOR DA EXISTÊNCIA DA OPÇÃO PELO SIMPLES.
    #  S - SIM
    #  N - NÃO
    #  EM BRANCO – OUTROS
    opcao_simples = Column(String(length=1))

    # DATA DE OPÇÃO PELO SIMPLES
    data_opcao_simples = Column(Date)

    # DATA DE EXCLUSÃO DO SIMPLES
    data_exclusao = Column(Date)

    # INDICADOR DA EXISTÊNCIA DA OPÇÃO PELO MEI
    #  S - SIM
    #  N - NÃO
    #  EM BRANCO - OUTROS
    opcao_mei = Column(String(length=1))

    # DATA DE OPÇÃO PELO MEI
    data_opcao_mei = Column(Date)

    # DATA DE EXCLUSÃO DO MEI
    data_exclusao_mei = Column(Date)
