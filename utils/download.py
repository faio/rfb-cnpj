# ------------------------------------------------------------------------------#
#                                                                               |
#   UTILITARIO PARA FAZER O DOWNLOAD DOS ARQUIVOS DA RECEITA FEDERAL DO BRASIL  |
#                                                                               |
# ------------------------------------------------------------------------------#
import re
import os
import threading
import click


from urllib.request import urlopen
from urllib.parse import urljoin
from time import perf_counter, sleep


URL_BASE_RFB = 'http://200.152.38.155/CNPJ/'


def get_urls(return_group: bool = True) -> str:
    """
    Retorna todas as urls dos arquivos da receita
    :param return_group: Caso seja true, concatena todas as urls, caso seja false
                         irá retornar separadamente as urls de empresa,
                         estabelecimento e socio
    :return:
    """

    # Baixa a página de download da receita
    data = str(urlopen(URL_BASE_RFB).read(), encoding='utf8')

    # Pega todas as urls
    urls = re.findall(r'href=[\'"]?([^\'" >]+)', data)

    # Filtra peloas arquivos que terminam com .zip
    urls = [url for url in urls if url.endswith('.zip')]

    # Pega apenas os que são necessários, que são os arquivos de sócios, empresas e canes
    empresa_urls = [url for url in urls if url.endswith('EMPRECSV.zip')]
    estabelecimento_urls = [url for url in urls if url.endswith('ESTABELE.zip')]
    socio_urls = [url for url in urls if url.endswith('SOCIOCSV.zip')]
    dados_simples_urls = [url for url in urls if url.find('SIMPLES') > 0]
    canes_urls = [url for url in urls if url.endswith('CNAECSV.zip')]
    pais_urls = [url for url in urls if url.endswith('PAISCSV.zip')]
    qualificacao_urls = [url for url in urls if url.endswith('QUALSCSV.zip')]
    natureza_urls = [url for url in urls if url.endswith('NATJUCSV.zip')]
    municipios_urls = [url for url in urls if url.endswith('MUNICCSV.zip')]

    if return_group:
        return empresa_urls + estabelecimento_urls + socio_urls + dados_simples_urls\
               + canes_urls + pais_urls + qualificacao_urls + natureza_urls + municipios_urls
    return empresa_urls, estabelecimento_urls, socio_urls, dados_simples_urls, \
           canes_urls + pais_urls + qualificacao_urls + natureza_urls + municipios_urls


def download(url, path=''):
    def get_length(meta):
        for k, v in meta._headers:
            if str(k).lower() == 'content-length':
                return int(v)

        return None

    file_name = url.split('/')[-1]  # Nome do arquivo
    url_byte = urlopen(url)
    meta = url_byte.info()
    factor_convert_mb = 1e6
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
            velocity = file_size_dl // (perf_counter() - start) / 100000
            percent = file_size_dl * 100. / file_size
            status = f"\rDownloading {file_name}: {file_size_dl_mb:10.2f}/{file_size_mb:2.2f} MB  [{percent:3.2f}%] " \
                     f"[{velocity:.3f} Mbps]"

            click.echo(status, nl=False)


def start_threads(path='download'):
    """
    Inicia o processo de download em Threads
    :param path: Caminho onde irá salvar os arquivos baixados, default: download
    :return:
    """
    file_list = get_urls()
    max_threads = len(file_list)
    thread_name = 'cnpj_download'
    tsleep = 0.05

    for i, file in enumerate(file_list):
        url = urljoin(URL_BASE_RFB, file)
        threading.Thread(target=download, args=[url, path], name=thread_name).start()

    dload_threads = [x.getName() for x in threading.enumerate() if thread_name == x.getName()]

    while len(dload_threads) >= max_threads:
        dload_threads = [x.getName() for x in threading.enumerate() if thread_name == x.getName()]
        sleep(tsleep)

    while dload_threads:
        dload_threads = [x.getName() for x in threading.enumerate() if thread_name == x.getName()]
        sleep(tsleep)


# if __name__ == '__main__':
#     start_threads()
