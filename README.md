## RFB CNPJ

* Projeto criado para tratar os dados vindo da Receita Federal do Brasil (RFB)   e converter os mesmos para um banco de dados suportado pela biblioteca SQLAlchemy.

**Motivação**

* A RFB mudou o formato de arquivo que disponibilizava os dados públicos de CNPJ  e com isso os sistema anteriores pararam de funcionar, anteriormente eu utilizava  a biblioteca https://github.com/fabioserpa/CNPJ-full que por muito tempo resolveu  o meu problema de tratar a base de dados e converter a mesma para um banco de dados relacional, com a mudança, a receita disponibizou os dados em um formato diferente e a biblioteca parou de funcionar. Resolvi criar essa biblioteca que já faz todo o processo de forma automática, baixando os dados da RFB, e realizando a conversão.

**Objetivos da biblioteca**  
  
* Realizar todo o processo de baixar e converter os dados disponibilizados pela RFB  de forma automática, sem precisar de intervenção humana em nenhuma etapa do processo.  
  
**Funções**  
  
 - Baixar os arquivos públicos disponibilizados pela RFB.
 - Converter os dados de empresa, estabelecimento, sócio, cnae, países, municípios qualificações, naturezas e dados do simples para um SGBD compatível com a biblioteca SQLAchemy.  
- Possibilidade de executar o processo em threads, melhorando significativamente a performance    

**OBS:**  
  
* Biblioteca construída buscando a menor dependência possível de libs externas.
* Requer python 3.7 ou superior, recomendado o python 3.9
* Para executar o sistema:        
  - Primeiro, instale as dependências:   
	
				> pip install -r requirements.txt

  - Depois execute o sistema:  
  
		> python main.py    
		
* Possíveis parametros:  

| Pârametro 		   | Default 			  | Decrição 									|
|    --                |--                    |--                                           |
| --help    		   |  -					  | Exibe a guia de ajuda						|
| --baixar 			   | true 	   			  | Ativa ou desativa o download dos dados no site da RFB 																						|
| --threads 		   | true     			  | ativa ou desativa o processo em threads.  	|
| --diretorio_arquivos | ./download 		  | Pasta de destino dos arquivos de download e/ou onde se localiza os arquivos da RFB 														|
| --database_url 	   | sqlite:///db.sqlite3 | URL de conexão com o SGBD no formato exigido pela biblioteca SQLAchemy																	|

      OBS: 
      - no banco SQLite ocorreu erro ao executar o mesmo em threads, no postgreSQL funcionou corretamente o processo.
      - Processo testado apenas no SQLite e no PostgreSQL
