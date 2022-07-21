import click
import logging

from importlib import import_module
from multiprocessing import Pool
from rfb.utils import download
from rfb.utils.convert_database import ConvertDatabase


log = logging.getLogger('rfb')
log.setLevel(logging.INFO)
logging.basicConfig(filename='rfb.log', format='%(levelname)s: %(name)s: %(asctime)s - %(message)s')


def run_insert(database_url: str, diretorio_arquivos: str, function_params: dict):
    """
    Função auxiliar para permitir executar ou não em threads as inserções no banco
    de dados
    :param database_url: URL de conexão com o banco de dados
    :param diretorio_arquivos: Diretório base dos arquivos CSV
    :param run_in_singleton: Não é para fazer a inserção de forma pararela na base de dados
    """
    module, cls = function_params['model'].rsplit('.', maxsplit=1)
    module = import_module(module)
    model = getattr(module, cls)

    function_params['model'] = model
    ConvertDatabase(database_url, diretorio_arquivos).populate(**function_params)


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

    msg = f"""
        Iniciando com os parâmetros:
            baixar: {baixar}
            threads: {threads}
            diretorio_arquivos: {diretorio_arquivos}
            database_url: {database_url}
        """
    log.info(msg)
    click.secho(msg)

    if baixar:
        process = None if threads else 1
        download.start_download(diretorio_arquivos, process=process)

    # Verificando se é para rodar sem o uso de paralerismo
    # OBS: SQLite não suporta paralelismo
    run_in_singleton = database_url.startswith('sqlite') or not threads

    convert_database = ConvertDatabase(database_url, diretorio_arquivos)
    convert_database.create_tables()  # Cria as tabelas

    params = [
        {'pattern_name': 'cnae', 'qt_column': 2, 'model': 'rfb.models.Cnae'},
        {'pattern_name': 'motivo_cadastral', 'qt_column': 2, 'model': 'rfb.models.MotivoCadastral'},
        {'pattern_name': 'municipio', 'qt_column': 2, 'model': 'rfb.models.Municipio'},
        {'pattern_name': 'natureza', 'qt_column': 2, 'model': 'rfb.models.Natureza'},
        {'pattern_name': 'pais', 'qt_column': 2, 'model': 'rfb.models.Pais'},
        {'pattern_name': 'qualificacao', 'qt_column': 2, 'model': 'rfb.models.Qualificacao'},
        {'pattern_name': 'dado_simples', 'qt_column': 7, 'model': 'rfb.models.DadoSimples'},
        {'pattern_name': 'socio', 'qt_column': 11, 'model': 'rfb.models.Socio'},
        {'pattern_name': 'empresa', 'qt_column': 7, 'model': 'rfb.models.Empresa'},
        {'pattern_name': 'estabelecimento', 'qt_column': 30, 'model': 'rfb.models.Estabelecimento'},
    ]

    process = 1 if run_in_singleton else len(params)

    with Pool(process) as pool:
        args = []
        for param in params:
            args.append([database_url, diretorio_arquivos, param])

        pool.starmap(run_insert, args)


if __name__ == '__main__':
    start()
