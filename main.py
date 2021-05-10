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
@click.option("--diretorio_arquivos", show_default=True, default='download',
              type=click.STRING, help="Pasta de destino dos arquivos de download")
@click.option("--database_url", show_default=True, default='sqlite:///db.sqlite3',
              type=click.STRING, help="URL de conexão do banco de dados")
def start(baixar, threads, diretorio_arquivos, database_url):

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
        'populate_socio'
    ]

    thread_name = 'cnpj_insert'
    tsleep = 0.05

    for function in functions:
        if threads:
            threading.Thread(
                target=run_insert,
                args=[function, database_url, diretorio_arquivos],
                name=thread_name
            ).start()
        else:
            run_insert(function, database_url, diretorio_arquivos)

    if threads:
        threads_runinngs = [x.getName() for x in threading.enumerate() if thread_name == x.getName()]

        while len(threads_runinngs) >= len(functions):
            threads_runinngs = [x.getName() for x in threading.enumerate() if thread_name == x.getName()]
            sleep(tsleep)

        while threads_runinngs:
            threads_runinngs = [x.getName() for x in threading.enumerate() if thread_name == x.getName()]
            sleep(tsleep)


if __name__ == '__main__':
    start()
