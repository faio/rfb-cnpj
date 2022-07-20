# ------------------------------------------------------------------------------#
#                                                                               |
#        UTILITARIO PARA CONVERTER OS DADOS PARA O BANCO DE DADOS               |
#                                                                               |
# ------------------------------------------------------------------------------#

import click
import settings

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.dados_simples import DadoSimples
from models.empresa import Empresa
from models.estabelecimento import Estabelecimento
from models.socio import Socio
from models.pais import Pais
from models.municipio import Municipio
from models.qualificacao import Qualificacao
from models.natureza import Natureza
from models.cnae import Cnae
from models.motivo_cadastral import MotivoCadastral
from pathlib import Path
from zipfile import ZipFile
from utils import convert


class ConvertDatabase:
    """
    Classe responsável por manipular os dados entre o arquivo e o banco
    de dados
    """

    def __init__(self, database_url: str, directory: str):
        """
        :param database_url: URL de conexão com o banco de dados
        :param directory: Diretório onde está os arquivos CSV
        """

        engine_kwargs = {
            'url': database_url,
            'echo': False,
            'future': True,
            'encoding': settings.ENCODING
        }

        self.engine = create_engine(**engine_kwargs)
        self.directory = directory
        self.session = sessionmaker(bind=self.engine)()

    def create_tables(self):
        """
        Cria as tabelas da bases de dados
        """
        Empresa().metadata.create_all(self.engine)
        Estabelecimento().metadata.create_all(self.engine)
        DadoSimples().metadata.create_all(self.engine)
        Socio().metadata.create_all(self.engine)
        Cnae().metadata.create_all(self.engine)
        Pais().metadata.create_all(self.engine)
        Municipio().metadata.create_all(self.engine)
        Qualificacao().metadata.create_all(self.engine)
        Natureza().metadata.create_all(self.engine)
        MotivoCadastral().metadata.create_all(self.engine)

    def read_file(self, path: str):
        """
        Faz a leitura do arquivo ZIP sem descompactar o mesmo retornando a linha
        indivualmente de cada um
        :param path:
        :return:
        """
        file = ZipFile(path, 'r')

        for name in file.namelist():
            content = file.open(name, mode='r')

            for line in content:
                row = str(line, encoding=settings.ENCODING, errors='replace')
                row = row.replace('\n', '').replace('\0', '')[1:-1].split('";"')
                yield row

    def populate_empresa(self):
        """
        Preenche os dados da tabela empresa
        :return:
        """

        path = Path(self.directory)
        files_csvs = sorted(str(p) for p in path.iterdir() if p.name.startswith('Empresas'))
        empresas_cache = []

        for file in files_csvs:
            click.echo(f'[EMPRESA] Importando o CSV {file}', nl=True)
            for i, data in enumerate(self.read_file(file)):

                if len(data) != 7:
                    raise ValueError(
                        f'[EMPRESA] Erro de integridade na leitura do arquivo, linha {i} arquivo {file}'
                    )

                empresa = Empresa()
                empresa.cnpj = data[0] or None
                empresa.razao = data[1] or None
                empresa.natureza = convert.parse_int(data[2])
                empresa.qualificacao_pf = convert.parse_int(data[3])
                empresa.capital = convert.parse_float(data[4])
                empresa.porte = convert.parse_int(data[5])
                empresa.ente_federativo = convert.parse_int(data[6])
                empresas_cache.append(empresa)

                if i > 0 and i % settings.CHUNK_ROWS_INSERT_DATABASE == 0:
                    click.echo(f'[EMPRESA] Inserindo o registro {i} do arquivo {file}', nl=True)
                    self.session.bulk_save_objects(empresas_cache)
                    self.session.commit()
                    empresas_cache = []

            if empresas_cache:
                self.session.bulk_save_objects(empresas_cache)
                self.session.commit()
                empresas_cache = []

        if empresas_cache:
            self.session.bulk_save_objects(empresas_cache)
            self.session.commit()

        click.echo('[EMPRESA] Finalizado a inserção dos dados de empresas', nl=True)

    def populate_estabelecimento(self):
        """
        Preenche os dados da tabela estabelecimento
        :return:
        """

        path = Path(self.directory)
        files_csvs = sorted(str(p) for p in path.iterdir() if p.name.startswith('Estabelecimentos'))
        estabelecimentos_cache = []

        for file in files_csvs:
            click.echo(f'[ESTABELECIMENTO] Importando o CSV {file}', nl=True)
            for i, data in enumerate(self.read_file(file)):

                if len(data) != 30:
                    raise ValueError(
                        f'[ESTABELECIMENTO] Erro de integridade na leitura do arquivo, linha {i} arquivo {file}'
                    )

                estabelecimento = Estabelecimento()
                estabelecimento.cnpj = data[0] or None
                estabelecimento.cnpj_ordem = data[1] or None
                estabelecimento.cnpj_dv = data[2] or None
                estabelecimento.matriz_filial = convert.parse_int(data[3])
                estabelecimento.nome = data[4] or None
                estabelecimento.situacao = convert.parse_int(data[5])
                estabelecimento.data_situacao = convert.parse_date(data[6])
                estabelecimento.motivo_situacao = data[7] or None
                estabelecimento.cidade_exterior = data[8] or None
                estabelecimento.pais = convert.parse_int(data[9])
                estabelecimento.inicio_atividade = convert.parse_date(data[10])
                estabelecimento.cnae_fiscal = data[11] or None
                estabelecimento.cnae_secundario = data[12] or None
                estabelecimento.tipo_logradouro = data[13] or None
                estabelecimento.logradouro = data[14] or None
                estabelecimento.numero = data[15] or None
                estabelecimento.complemento = data[16] or None
                estabelecimento.bairro = data[17] or None
                cep = convert.only_number(data[18])
                estabelecimento.cep = cep if len(cep) == 8 else None
                # Algumas UF estão com os dados errados vindo da RFB
                estabelecimento.uf = data[19] or None if len(data[19]) <= 2 else None
                estabelecimento.municipio = convert.parse_int(data[20])
                estabelecimento.ddd_1 = convert.parse_int(data[21])
                estabelecimento.telefone_1 = convert.only_number(data[22])
                estabelecimento.ddd_2 = convert.parse_int(data[23])
                estabelecimento.telefone_2 = convert.only_number(data[24])
                estabelecimento.ddd_fax = convert.parse_int(data[25])
                estabelecimento.numero_fax = convert.only_number(data[26])
                estabelecimento.email = data[27] or None
                estabelecimento.situacao_especial = data[28] or None
                estabelecimento.data_situacao_especial = convert.parse_date(data[29])

                estabelecimentos_cache.append(estabelecimento)

                if i > 0 and i % settings.CHUNK_ROWS_INSERT_DATABASE == 0:
                    click.echo(f'[ESTABELECIMENTO] Inserindo o registro {i} do arquivo {file}', nl=True)
                    self.session.bulk_save_objects(estabelecimentos_cache)
                    self.session.commit()
                    estabelecimentos_cache = []

            if estabelecimentos_cache:
                self.session.bulk_save_objects(estabelecimentos_cache)
                self.session.commit()
                estabelecimentos_cache = []

        if estabelecimentos_cache:
            self.session.bulk_save_objects(estabelecimentos_cache)
            self.session.commit()

        click.echo('[ESTABELECIMENTO] Finalizado a inserção dos dados de estabelecimento', nl=True)

    def populate_dado_simples(self):
        """
        Preenche os dados da tabela de simples nacional
        :return:
        """

        path = Path(self.directory)
        files_csvs = sorted(str(p) for p in path.iterdir() if p.name == 'Simples.zip')
        dados_simples_cache = []

        for file in files_csvs:
            click.echo(f'[DADO SIMPLES] Importando o CSV {file}', nl=True)
            for i, data in enumerate(self.read_file(file)):

                if len(data) != 7:
                    raise ValueError(
                        f'[DADO SIMPLES] Erro de integridade na leitura do arquivo, linha {i} arquivo {file}'
                    )

                dados_simples = DadoSimples()
                dados_simples.cnpj = data[0] or None
                dados_simples.opcao_simples = data[1] or None
                dados_simples.data_opcao_simples = convert.parse_date(data[2])
                dados_simples.data_exclusao = convert.parse_date(data[3])
                dados_simples.opcao_mei = data[4] or None
                dados_simples.data_opcao_mei = convert.parse_date(data[5])
                dados_simples.data_exclusao_mei = convert.parse_date(data[6])

                dados_simples_cache.append(dados_simples)

                if i > 0 and i % settings.CHUNK_ROWS_INSERT_DATABASE == 0:
                    click.echo(f'[DADO SIMPLES] Inserindo o registro {i} do arquivo {file}', nl=True)
                    self.session.bulk_save_objects(dados_simples_cache)
                    self.session.commit()
                    dados_simples_cache = []

            if dados_simples_cache:
                self.session.bulk_save_objects(dados_simples_cache)
                self.session.commit()
                dados_simples_cache = []

        if dados_simples_cache:
            self.session.bulk_save_objects(dados_simples_cache)
            self.session.commit()

        click.echo('[DADO SIMPLES] Finalizado a inserção dos dados de simples nacional', nl=True)

    def populate_socio(self):
        """
        Preenche os dados da tabela de Sócios
        :return:
        """

        path = Path(self.directory)
        files_csvs = sorted(str(p) for p in path.iterdir() if p.name.startswith('Socios'))
        socio_cache = []

        for file in files_csvs:
            click.echo(f'[SOCIO] Importando o CSV {file}', nl=True)
            for i, data in enumerate(self.read_file(file)):

                if len(data) != 11:
                    raise ValueError(
                        f'[SOCIO] Erro de integridade na leitura do arquivo, linha {i} arquivo {file}'
                    )

                socio = Socio()
                socio.cnpj = data[0] or None
                socio.identificador_socio = convert.parse_int(data[1])
                socio.nome = data[2] or None
                socio.cpf_cnpj = data[3] or None
                socio.qualificacao = convert.parse_int(data[4])
                socio.data_entrada_sociedade = convert.parse_date(data[5])
                socio.codigo_pais = convert.parse_int(data[6])
                socio.cpf_representante_legal = data[7] or None
                socio.nome_representante_legal = data[8] or None
                socio.qualificacao_representante_legal = convert.parse_int(data[9])
                socio.faixa_etaria = data[10] or None

                socio_cache.append(socio)

                if i > 0 and i % settings.CHUNK_ROWS_INSERT_DATABASE == 0:
                    click.echo(f'[SOCIO] Inserindo o registro {i} do arquivo {file}', nl=True)
                    self.session.bulk_save_objects(socio_cache)
                    self.session.commit()
                    socio_cache = []

            if socio_cache:
                self.session.bulk_save_objects(socio_cache)
                self.session.commit()
                socio_cache = []

        if socio_cache:
            self.session.bulk_save_objects(socio_cache)
            self.session.commit()

        click.echo('[SOCIO] Finalizado a inserção dos dados de sócios', nl=True)

    def populate_paises(self):
        """
        Preenche os dados da tabela de PAISES
        :return:
        """

        path = Path(self.directory)
        files_csvs = sorted(str(p) for p in path.iterdir() if p.name == 'Paises.zip')
        pais_cache = []

        for file in files_csvs:
            click.echo(f'[PAIS] Importando o CSV {file}', nl=True)
            for i, data in enumerate(self.read_file(file)):

                if len(data) != 2:
                    raise ValueError(
                        f'[PAIS] Erro de integridade na leitura do arquivo, linha {i} arquivo {file}'
                    )

                pais = Pais()
                pais.codigo = convert.parse_int(data[0])
                pais.descricao = data[1] or None

                pais_cache.append(pais)

        if pais_cache:
            self.session.bulk_save_objects(pais_cache)
            self.session.commit()

        click.echo('[PAIS] Finalizado a inserção dos dados de paises', nl=True)

    def populate_municipios(self):
        """
        Preenche os dados da tabela de Municipios
        :return:
        """

        path = Path(self.directory)
        files_csvs = sorted(str(p) for p in path.iterdir() if p.name == 'Municipios.zip')
        municipios_cache = []

        for file in files_csvs:
            click.echo(f'[MUNICIPIO] Importando o CSV {file}', nl=True)
            for i, data in enumerate(self.read_file(file)):

                if len(data) != 2:
                    raise ValueError(
                        f'[MUNICIPIO] Erro de integridade na leitura do arquivo, linha {i} arquivo {file}'
                    )

                municipio = Municipio()
                municipio.codigo = data[0] or None
                municipio.descricao = data[1] or None

                municipios_cache.append(municipio)

        if municipios_cache:
            self.session.bulk_save_objects(municipios_cache)
            self.session.commit()

        click.echo('[MUNICIPIO] Finalizado a inserção dos dados de municipio', nl=True)

    def populate_qualificacoes(self):
        """
        Preenche os dados da tabela de qualificação dos sócios
        :return:
        """

        path = Path(self.directory)
        files_csvs = sorted(str(p) for p in path.iterdir() if p.name == 'Qualificacoes.zip')
        qualificacao_cache = []

        for file in files_csvs:
            click.echo(f'[QUALIFICACAO] Importando o CSV {file}', nl=True)
            for i, data in enumerate(self.read_file(file)):

                if len(data) != 2:
                    raise ValueError(
                        f'[QUALIFICACAO] Erro de integridade na leitura do arquivo, linha {i} arquivo {file}'
                    )

                qualificacao = Qualificacao()
                qualificacao.codigo = convert.parse_int(data[0])
                qualificacao.descricao = data[1] or None

                qualificacao_cache.append(qualificacao)

        if qualificacao_cache:
            self.session.bulk_save_objects(qualificacao_cache)
            self.session.commit()

        click.echo('[QUALIFICACAO] Finalizado a inserção dos dados de qualificacao', nl=True)

    def populate_naturezas(self):
        """
        Preenche os dados da tabela de natuezas juridicas
        :return:
        """

        path = Path(self.directory)
        files_csvs = sorted(str(p) for p in path.iterdir() if p.name == 'Naturezas.zip')
        naturezas_cache = []

        for file in files_csvs:
            click.echo(f'[NATUREZA] Importando o CSV {file}', nl=True)
            for i, data in enumerate(self.read_file(file)):

                if len(data) != 2:
                    raise ValueError(
                        f'[NATUREZA] Erro de integridade na leitura do arquivo, linha {i} arquivo {file}'
                    )

                natureza = Natureza()
                natureza.codigo = convert.parse_int(data[0])
                natureza.descricao = data[1] or None

                naturezas_cache.append(natureza)

        if naturezas_cache:
            self.session.bulk_save_objects(naturezas_cache)
            self.session.commit()

        click.echo('[NATUREZA] Finalizado a inserção dos dados natureza jurídica', nl=True)

    def populate_cnae(self):
        """
        Preenche os dados da tabela de CNAEs
        :return:
        """

        path = Path(self.directory)
        files_csvs = sorted(str(p) for p in path.iterdir() if p.name == 'Cnaes.zip')
        cnae_cache = []

        for file in files_csvs:
            click.echo(f'[CNAE] Importando o CSV {file}', nl=True)
            for i, data in enumerate(self.read_file(file)):

                if len(data) != 2:
                    raise ValueError(
                        f'[CNAE] Erro de integridade na leitura do arquivo, linha {i} arquivo {file}'
                    )

                cnae = Cnae()
                cnae.codigo = data[0] or None
                cnae.descricao = data[1] or None

                cnae_cache.append(cnae)

        if cnae_cache:
            self.session.bulk_save_objects(cnae_cache)
            self.session.commit()

        click.echo('[CNAE] Finalizado a inserção dos dados de CNAE', nl=True)

    def populate_motivo_cadastral(self):
        """
        Preenche os dados da tabela de motivo cadastral
        :return:
        """

        path = Path(self.directory)
        files_csvs = sorted(str(p) for p in path.iterdir() if p.name == 'Motivos.zip')
        motivo_cadastral_cache = []

        for file in files_csvs:
            click.echo(f'[MOTIVACAO_CADASTRAL] Importando o CSV {file}', nl=True)
            for i, data in enumerate(self.read_file(file)):

                if len(data) != 2:
                    raise ValueError(
                        f'[MOTIVACAO_CADASTRAL] Erro de integridade na leitura do arquivo, linha {i} arquivo {file}'
                    )

                motivo_cadastral = MotivoCadastral()
                motivo_cadastral.codigo = convert.parse_int(data[0])
                motivo_cadastral.descricao = data[1] or None

                motivo_cadastral_cache.append(motivo_cadastral)

        if motivo_cadastral_cache:
            self.session.bulk_save_objects(motivo_cadastral_cache)
            self.session.commit()

        click.echo('[MOTIVACAO_CADASTRAL] Finalizado a inserção dos Motivos Cadastral', nl=True)
