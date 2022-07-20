import click
import threading

from time import sleep
from urllib.parse import urljoin
from utils import download
from utils.download import URL_BASE_RFB
from utils.convert_database import ConvertDatabase


def run_insert(function_name, database_url, diretorio_arquivos):
    """
    Função auxiliar para permitir executar ou não em threads as inserções no banco
    de dados
    :param function_name: Nome da função dentro de ConvertDatabase
    :param database_url: URL de conexão com o banco de dados
    :param diretorio_arquivos: Diretório base dos arquivos CSV
    """
    convert_database = ConvertDatabase(database_url, diretorio_arquivos)
    getattr(convert_database, function_name)()


@click.command()
@click.option("--baixar", show_default=True, default=True, type=click.BOOL,
              help="É para baixar os arquivos?")
@click.option("--threads", show_default=True, default=True, type=click.BOOL,
              help="É para ser executado em Threads?")
@click.option("--diretorio_arquivos", "--diretorio", "--diretorio-arquivos",
              show_default=True, default='download',
              type=click.Path(), help="Pasta de destino dos arquivos de download")
@click.option("--database_url", "--database", "--database-url", type=click.STRING, default=None,
              help="URL de conexão do banco de dados")
def start(baixar, threads, diretorio_arquivos, database_url):

    if database_url is None:
        if click.prompt(
            "Não foi informado a url de conexão com o banco de dados, deseja utilizar o SQLite?",
            show_choices=True,
            type=click.Choice(['Y', 'N'], case_sensitive=False)
        ) == 'Y':
            database_url = 'sqlite:///db.sqlite3'
        else:
            database_url = click.prompt(
                "Informe e confirme a url de conexão com o banco de dados: ",
                confirmation_prompt=True,
                type=click.STRING
            )

    click.secho(
        f"""
        Iniciando com os parâmetros:
            baixar: {baixar}
            threads: {threads}
            diretorio_arquivos: {diretorio_arquivos}
            database_url: {database_url}
        """
    )

    if baixar:
        if threads:
            download.start_threads(diretorio_arquivos)
        else:
            for url in download.get_urls():
                download.download(urljoin(URL_BASE_RFB, url), diretorio_arquivos)

    convert_database = ConvertDatabase(database_url, diretorio_arquivos)
    convert_database.create_tables()  # Cria as tabelas

    # Nomes das funções de inserção de dados
    functions = [
        'populate_cnae',
        'populate_paises',
        'populate_municipios',
        'populate_qualificacoes',
        'populate_naturezas',
        'populate_empresa',
        'populate_estabelecimento',
        'populate_dado_simples',
        'populate_socio',
        'populate_motivo_cadastral'
    ]

    thread_name = 'cnpj_insert'
    tsleep = 0.05

    # Verificando se é para rodar sem usar as threads
    # OBS: SQLite não suporta muitas threads, por isso, evita rodar o mesmo em threads
    run_in_singleton = database_url.startswith('sqlite') or not threads

    for function in functions:
        if not run_in_singleton:
            threading.Thread(
                target=run_insert,
                args=[function, database_url, diretorio_arquivos],
                name=thread_name
            ).start()
        else:
            run_insert(function, database_url, diretorio_arquivos)

    if not run_in_singleton:
        threads_runinngs = [x.getName() for x in threading.enumerate() if thread_name == x.getName()]

        while len(threads_runinngs) >= len(functions):
            threads_runinngs = [x.getName() for x in threading.enumerate() if thread_name == x.getName()]
            sleep(tsleep)

        while threads_runinngs:
            threads_runinngs = [x.getName() for x in threading.enumerate() if thread_name == x.getName()]
            sleep(tsleep)


if __name__ == '__main__':
    start()
