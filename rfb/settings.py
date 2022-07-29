# Encoding do arquivo recebido pela RFB e do SGBD que será criado
ENCODING = 'ISO-8859-1'

# Tamanho dos buffer no momento de persistir os dados no SGBD
CHUNK_ROWS_INSERT_DATABASE = 100_000

# Máxima de tentativas de download
MAX_RETRY_DOWNLOAD = 100

# URL da receita federal onde está os arquivos
URL_BASE_RFB = 'http://200.152.38.155/CNPJ/'
