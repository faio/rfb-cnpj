# ------------------------------------------------------------------------------#
#                                                                               |
#   UTILITARIO PARA FAZER O DOWNLOAD DOS ARQUIVOS DA RECEITA FEDERAL DO BRASIL  |
#                                                                               |
# ------------------------------------------------------------------------------#
import re
import os
import click

from typing import Optional
from logging import getLogger
from multiprocessing import Pool
from urllib.request import urlopen
from urllib.parse import urljoin
from time import perf_counter
from rfb.utils import NAMES_PATTERNS
from rfb.settings import MAX_RETRY_DOWNLOAD, URL_BASE_RFB


log = getLogger(__name__)


def _get_urls() -> list:
    """ Retorna todas as urls/nomes dos arquivos da receita """

    # Baixa a página de download da receita
    data = str(urlopen(URL_BASE_RFB).read(), encoding='utf8')

    # Pega todas as urls que foram retornadas
    all_urls = re.findall(r'href=[\'"]?([^\'" >]+)', data)

    # Filtra pelas urls que terminam com .zip
    all_urls_zip = [url for url in all_urls if url.endswith('.zip')]

    urls = []
    for pattern in NAMES_PATTERNS.values():
        urls.extend(
            filter(lambda u: u.startswith(pattern), all_urls_zip)
        )

    return urls


def _download(url: str, path: str = '', retry_count: int = 0) -> None:
    """
    Faz o download de algum arquivo
    :param url:
        URL de onde se encontra o arquivo

    :param path:
        Caminho raiz aonde será salvo o arquivo

    :param retry_count:
        Parâmetro para realizar a contagem recursiva da quantidade de
        tentativas que foi executada, não informar
    """
    def get_length(meta):
        for k, v in meta._headers:
            if str(k).lower() == 'content-length':
                return int(v)

        return None

    if retry_count >= MAX_RETRY_DOWNLOAD:
        msg = f'Erro ao baixar o arquivo {url}! Número máximo de {MAX_RETRY_DOWNLOAD} tentativas alcançado!'
        click.echo(msg, err=True)
        log.error(msg)
        raise Exception(msg)

    file_name = url.split('/')[-1]  # Nome do arquivo
    url_byte = urlopen(url)
    meta = url_byte.info()
    factor_convert_mb = 1048576
    file_size = get_length(meta)  # Tamanho do arquivo
    file_size_mb = file_size / factor_convert_mb  # Tamanho do arquivo em byte

    file_size_dl = 0  # tamanho já baixado
    block_sz = 8192  # Tamanho do buffer de cada download
    start = perf_counter()

    dir = os.path.join(path, file_name)
    if path and not os.path.isdir(path):
        os.mkdir(path)

    with open(dir, 'wb') as file_buffer:
        while True:
            buffer = url_byte.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            file_size_dl_mb = file_size_dl / factor_convert_mb
            file_buffer.write(buffer)
            velocity = file_size_dl // (perf_counter() - start) / factor_convert_mb
            percent = file_size_dl * 100. / file_size
            status = f"\rDownloading {file_name}: {file_size_dl_mb:10.2f}/{file_size_mb:2.2f} MB  [{percent:3.2f}%] " \
                     f"[{velocity:.3f} Mbps]"

            click.echo(status, nl=False)

    if file_size_dl == file_size:
        click.echo(f'Download do arquivo {url} baixado com sucesso com {retry_count + 1} tentativas!')
    else:  # Então, ocorreu algum erro com o download, recomeça!
        os.remove(dir)
        msg = f'Erro ao baixar o arquivo {url}, tamanho baixado: {file_size_dl}, '\
              f'tamanho esperado {file_size}, tentativa de número {retry_count + 1}'
        log.warning(msg)
        click.echo(msg, err=True)
        _download(url, path, retry_count=retry_count + 1)


def start_download(path='download', process: Optional[int] = None) -> None:
    """
    Inicia o processo de download de forma paralera
    :param path: Caminho onde irá salvar os arquivos baixados, default: download
    :param process: Quantidade de processos que será utilizado na Pool
    """
    file_list = _get_urls()

    msg = 'Iniciando o download dos arquivos'
    log.info(msg)
    click.echo(msg)

    process = len(file_list) if process is None else process

    with Pool(process) as pool:
        args = []
        for i, file in enumerate(file_list):
            url = urljoin(URL_BASE_RFB, file)
            args.append([url, path])

        pool.starmap(_download, args)
