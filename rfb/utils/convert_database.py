# ------------------------------------------------------------------------------#
#                                                                               |
#        UTILITARIO PARA CONVERTER OS DADOS PARA O BANCO DE DADOS               |
#                                                                               |
# ------------------------------------------------------------------------------#

from asyncio.log import logger
from sqlite3 import IntegrityError
import click
from rfb import settings

from typing import Optional
from logging import getLogger

from sqlalchemy import create_engine, insert, null
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.decl_api import DeclarativeMeta

from rfb.models import DadoSimples
from rfb.models import Empresa
from rfb.models import Estabelecimento
from rfb.models import Socio
from rfb.models import Pais
from rfb.models import Municipio
from rfb.models import Qualificacao
from rfb.models import Natureza
from rfb.models import Cnae
from rfb.models import MotivoCadastral
from rfb.models import Cidade
from pathlib import Path, PurePath
from zipfile import ZipFile
from rfb.utils import NAMES_PATTERNS
from rfb.utils import convert

log = getLogger(__name__)


def read_file(path: str) -> list:
    """
    Faz a leitura do arquivo ZIP sem descompactar o mesmo retornando a linha lida
    :param path: Caminho do arquivo que será lido
    :return: lista na qual cada elemento representa uma coluna da linha lida
    """

    file = ZipFile(path, 'r')

    for name in file.namelist():
        content = file.open(name, mode='r')

        for line in content:
            rowLine = line.strip().decode(encoding=settings.ENCODING, errors='replace')
            rowLine = rowLine.replace('\n', '')
            row = rowLine.replace('";"', '||;').replace('"', '').split('||;')
            if (len(row) <= 1):
                row = rowLine.replace('"', '').split(';')
            yield row


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
        Cidade().metadata.create_all(self.engine)

    def parse_empresa(self, row: list) -> dict:
        """ Faz o parse e tratamento da linha do arquivo em um dict compativo com models.Empresa """

        return {
            'cnpj': row[0] or None,
            'razao': row[1] or None,
            'natureza': convert.parse_int(row[2]),
            'qualificacao_pf': convert.parse_int(row[3]),
            'capital': convert.parse_float(row[4]),
            'porte': convert.parse_int(row[5]),
            'ente_federativo': convert.parse_int(row[6]),
        }

    def parse_estabelecimento(self, row: list) -> dict:
        """ Faz o parse e tratamento da linha do arquivo em um dict compativo com models.Estabelecimento """

        cep = convert.only_number(row[18])
        cep = cep if len(cep) == 8 else None

        # Algumas UF estão com os dados errados vindo da RFB
        uf = row[19] or None if len(row[19]) <= 2 else None

        return {
            'cnpj': row[0] or None,
            'cnpj_ordem': row[1] or None,
            'cnpj_dv': row[2] or None,
            'matriz_filial': convert.parse_int(row[3]),
            'nome': row[4] or None,
            'situacao': convert.parse_int(row[5]),
            'data_situacao': convert.parse_date(row[6]),
            'motivo_situacao': row[7] or None,
            'cidade_exterior': row[8] or None,
            'pais': convert.parse_int(row[9]),
            'inicio_atividade': convert.parse_date(row[10]),
            'cnae_fiscal': row[11] or None,
            'cnae_secundario': row[12] or None,
            'tipo_logradouro': row[13] or None,
            'logradouro': row[14] or None,
            'numero': row[15] or None,
            'complemento': row[16] or None,
            'bairro': row[17] or None,
            'cep': cep,
            'uf': uf,
            'municipio': convert.parse_int(row[20]),
            'ddd_1': convert.parse_int(row[21]),
            'telefone_1': convert.only_number(row[22]),
            'ddd_2': convert.parse_int(row[23]),
            'telefone_2': convert.only_number(row[24]),
            'ddd_fax': convert.parse_int(row[25]),
            'numero_fax': convert.only_number(row[26]),
            'email': row[27] or None,
            'situacao_especial': row[28] or None,
            'data_situacao_especial': convert.parse_date(row[29]),
        }

    def parse_dado_simples(self, row: list) -> dict:
        """ Faz o parse e tratamento da linha do arquivo em um dict compativo com models.DadoSimples """

        return {
            'cnpj': row[0] or None,
            'opcao_simples': row[1] or None,
            'data_opcao_simples': convert.parse_date(row[2]),
            'data_exclusao': convert.parse_date(row[3]),
            'opcao_mei': row[4] or None,
            'data_opcao_mei': convert.parse_date(row[5]),
            'data_exclusao_mei': convert.parse_date(row[6]),
        }

    def parse_socio(self, row: list) -> dict:
        """ Faz o parse e tratamento da linha do arquivo em um dict compativo com models.Socio """

        return {
            'cnpj': row[0] or None,
            'identificador_socio': convert.parse_int(row[1]),
            'nome': row[2] or None,
            'cpf_cnpj': row[3] or None,
            'qualificacao': convert.parse_int(row[4]),
            'data_entrada_sociedade': convert.parse_date(row[5]),
            'codigo_pais': convert.parse_int(row[6]),
            'cpf_representante_legal': row[7] or None,
            'nome_representante_legal': row[8] or None,
            'qualificacao_representante_legal': convert.parse_int(row[9]),
            'faixa_etaria': row[10] or None,
        }

    def parse_pais(self, row: list) -> dict:
        """ Faz o parse e tratamento da linha do arquivo em um dict compativo com models.Pais """

        return {
            'codigo': convert.parse_int(row[0]),
            'descricao': row[1] or None
        }

    def parse_municipio(self, row: list) -> dict:
        """ Faz o parse e tratamento da linha do arquivo em um dict compativo com models.Municipio """

        return {
            'codigo': row[0],
            'descricao': row[1]
        }

    def parse_qualificacao(self, row: list) -> dict:
        """ Faz o parse e tratamento da linha do arquivo em um dict compativo com models.Qualificacao """

        return {
            'codigo': convert.parse_int(row[0]),
            'descricao': row[1] or None
        }

    def parse_natureza(self, row: list) -> dict:
        """ Faz o parse e tratamento da linha do arquivo em um dict compativo com models.Natureza """

        return {
            'codigo': convert.parse_int(row[0]),
            'descricao': row[1] or None
        }

    def parse_cnae(self, row: list) -> dict:
        """ Faz o parse e tratamento da linha do arquivo em um dict compativo com models.Cnae """

        return {
            'codigo': row[0] or None,
            'descricao': row[1] or None
        }

    def parse_motivo_cadastral(self, row: list) -> dict:
        """ Faz o parse e tratamento da linha do arquivo em um dict compativo com models.MotivoCadastral """

        return {
            'codigo': convert.parse_int(row[0]),
            'descricao': row[1] or None
        }

    def parse_cidade(self, row: list) -> dict:
        """ Faz o parse e tratamento da linha do arquivo em um dict compativo com models.Cidades """

        return {
            'cod_tom': convert.parse_int(row[5]),
            'nome': row[0] or None,
            'uf': row[1] or None,
            'ibge': row[2] or None,
            'latitude': row[3] or None,
            'longitude': row[4] or None
        }

    def populate(self,
                 pattern_name: str,
                 qt_column: int,
                 model: DeclarativeMeta,
                 parse_function: Optional[str] = None) -> None:
        """
        Preenche os dados da tabela de motivo cadastral

        :param pattern_name:
            Nome do pattern_name em utils.NAMES_PATTERNS

        :param qt_column:
            Quantidade de colunas que se espera que tenha cada linha

        :param model:
            Classe responsável pela manipulação dos dados no banco de dados

        :param parse_function:
            Nome da função responsável por fazer os parse da informação,
            caso não seja informado, será utilizado baseado no pattern_name
        """

        path = Path(self.directory)
        file_pattern_name = NAMES_PATTERNS[pattern_name]
        files_csvs = filter(lambda p: p.name.startswith(file_pattern_name) and p.name.endswith('.zip'), path.iterdir())
        files_csvs = sorted(files_csvs)
        populate_name = pattern_name.replace('_', ' ').upper()

        if parse_function is None:
            parse_function = f'parse_{pattern_name}'

        for file in files_csvs:
            self._execute(
                populate_name=populate_name,
                columns=qt_column,
                parse_function=parse_function,
                model=model,
                file=file
            )

        info = f'[{populate_name}] Finalizado a inserção dos { populate_name }'
        log.info(info)
        click.echo(info, nl=True)

    def _filter(self, arr):
        cache = []
        j = 0
        for item in arr:
            if len(cache) == 0:
                cache.append(item)
                pass
            else:
                for i, itemcache in enumerate(cache):
                    if itemcache['cnpj'] == item['cnpj']:
                        if len(str(item)) > len(str(itemcache)):
                            del cache[i]
                            cache.append(item)
                        j = 1
                if j == 0:
                    cache.append(item)
        return list(cache)

    def _commit(self, model: DeclarativeMeta, rows_cache: list):
        try:
            self.session.bulk_insert_mappings(model, rows_cache)
            self.session.commit()
        except:
            print("bulk inserting rows failed, fallback to one by one")
            rows = rows_cache
            for item in rows:
                try:
                    self.session.execute(insert(model).values(**item))
                    self.session.commit()
                except:
                    print("Error inserting item: %s", item)
                    self.session.rollback()
                    pass

    def _execute(self, file: PurePath, populate_name: str,
                 columns: int, model: DeclarativeMeta,
                 parse_function: Optional[str] = None):
        """
        Executa o insert no banco de dados

        :param file:
            Caminho do arquivo CSV que será lido

        :param columns:
            Quantidade de colunas que se espera que tenha cada linha

        :param model:
            Classe responsável pela manipulação dos dados no banco de dados

        :param parse_function:
            Nome da função responsável por fazer os parse da informação,
            caso não seja informado, será utilizado baseado no pattern_name
        """

        msg = f'[{populate_name}] Importando o CSV {file}'
        log.info(msg)
        click.echo(msg, nl=True)
        rows_cache = []
        parse_function = getattr(self, parse_function)

        for i, row in enumerate(read_file(file)):
            if len(row) != columns:
                msg = f'[{populate_name}] Erro de integridade na leitura do arquivo, linha {i} arquivo {file}! '\
                      f'Esperado {columns} e encontrado {len(row)}'
                log.error(msg)
                raise ValueError(msg)

            rows_cache.append(parse_function(row))

            if i > 0 and i % settings.CHUNK_ROWS_INSERT_DATABASE == 0:
                msg = f'[{populate_name}] Inserindo o registro { i + 1 } do arquivo {file}'
                log.debug(msg)
                click.echo(msg, nl=True)
                self._commit(model, rows_cache)
                rows_cache = []

        # Inserindo os resquícios de dados que podem ter ficado sem ser inseridos
        if rows_cache:
            self._commit(model, rows_cache)
