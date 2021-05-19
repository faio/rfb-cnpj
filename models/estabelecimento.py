from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Date

Base = declarative_base()


class Estabelecimento(Base):
    __tablename__ = 'estabelecimentos'

    id = Column(Integer, primary_key=True)

    # NÚMERO BASE DE INSCRIÇÃO NO CNPJ (OITO PRIMEIROS DÍGITOS
    # DO CNPJ).
    cnpj = Column(String(length=8))

    # NÚMERO DO ESTABELECIMENTO DE INSCRIÇÃO NO CNPJ (DO
    # NONO ATÉ O DÉCIMO SEGUNDO DÍGITO DO CNPJ).
    cnpj_ordem = Column(String(length=4))

    # DÍGITO VERIFICADOR DO NÚMERO DE INSCRIÇÃO NO CNPJ (DOIS
    # ÚLTIMOS DÍGITOS DO CNPJ).
    cnpj_dv = Column(String(length=2))

    # CORRESPONDE AO NOME FANTASIA
    nome = Column(String)

    # CÓDIGO DO IDENTIFICADOR MATRIZ/FILIAL:
    #       1 – MATRIZ
    #       2 – FILIAL
    matriz_filial = Column(Integer)

    # CÓDIGO DA SITUAÇÃO CADASTRAL:
    #      01 – NULA
    #      2 – ATIVA
    #      3 – SUSPENSA
    #      4 – INAPTA
    #      08 – BAIXADA
    situacao = Column(Integer)

    # DATA DO EVENTO DA SITUAÇÃO CADASTRA
    data_situacao = Column(Date)

    # CÓDIGO DO MOTIVO DA SITUAÇÃO CADASTRAL
    motivo_situacao = Column(String)

    # NOME DA CIDADE NO EXTERIOR
    cidade_exterior = Column(String)

    # CÓDIGO DO PAIS
    pais = Column(Integer)

    # DATA DE INÍCIO DA ATIVIDADE
    inicio_atividade = Column(Date)

    # CÓDIGO DA ATIVIDADE ECONÔMICA PRINCIPAL DO
    # ESTABELECIMENTO
    cnae_fiscal = Column(String)

    # CÓDIGO DA(S) ATIVIDADE(S) ECONÔMICA(S) SECUNDÁRIA(S) DO
    # ESTABELECIMENTO
    cnae_secundario = Column(String)

    # DESCRIÇÃO DO TIPO DE LOGRADOURO
    tipo_logradouro = Column(String)

    # NOME DO LOGRADOURO ONDE SE LOCALIZA O
    # ESTABELECIMENTO.
    logradouro = Column(String)

    # NÚMERO ONDE SE LOCALIZA O ESTABELECIMENTO. QUANDO
    # NÃO HOUVER PREENCHIMENTO DO NÚMERO HAVERÁ ‘S/N
    numero = Column(String)

    # COMPLEMENTO
    complemento = Column(String)

    # BAIRRO ONDE SE LOCALIZA O ESTABELECIMENTO.
    bairro = Column(String)

    # CÓDIGO DE ENDEREÇAMENTO POSTAL REFERENTE AO
    # LOGRADOURO NO QUAL O ESTABELECIMENTO ESTA LOCALIZADO
    cep = Column(String(length=8))

    # SIGLA DA UNIDADE DA FEDERAÇÃO EM QUE SE ENCONTRA O
    # ESTABELECIMENTO
    uf = Column(String(length=2))

    # CÓDIGO DO MUNICÍPIO DE JURISDIÇÃO ONDE SE ENCONTRA O
    # ESTABELECIMENTO
    municipio = Column(Integer)

    # CONTÉM O DDD 1
    ddd_1 = Column(String)

    # CONTÉM O NÚMERO DO TELEFONE 1
    telefone_1 = Column(String(length=11))

    # CONTÉM O DDD 2
    ddd_2 = Column(Integer)

    # CONTÉM O NÚMERO DO TELEFONE 2
    telefone_2 = Column(String(length=11))

    # CONTÉM O DDD DO FAX
    ddd_fax = Column(Integer)

    # CONTÉM O NÚMERO DO FAX
    numero_fax = Column(String(length=11))

    # CONTÉM O E-MAIL DO CONTRIBUINTE
    email = Column(String)

    # SITUAÇÃO ESPECIAL DA EMPRESA
    situacao_especial = Column(String)

    # DATA EM QUE A EMPRESA ENTROU EM SITUAÇÃO ESPECIAL
    data_situacao_especial = Column(Date)
