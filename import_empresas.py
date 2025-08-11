import mysql.connector
import os

# Caminho base e prefixo dos arquivos
diretorio = "C:/Users/User/Documents/Receita Federal/empresas/"
prefixo = "K3241.K03200Y"
sufixo = ".D50614.EMPRECSV"

# Gera a lista de arquivos Y0 a Y9
arquivos = [f"{prefixo}{i}{sufixo}" for i in range(10)]

# Conecta ao banco de dados
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='receita',
    allow_local_infile=True  # Habilita o uso do LOAD DATA LOCAL INFILE
)
cursor = conn.cursor()

# Cria a tabela se ainda não existir
cursor.execute("""
CREATE TABLE IF NOT EXISTS empresas (
    cnpj8 VARCHAR(8),
    razao_social VARCHAR(255),
    natureza_juridica VARCHAR(4),
    qualificacao_responsavel VARCHAR(3),
    capital_social VARCHAR(20),
    porte VARCHAR(1),
    ente_federativo VARCHAR(7)
)
""")

# Processa os arquivos
for nome_arquivo in arquivos:
    caminho_arquivo = os.path.join(diretorio, nome_arquivo)
    print(f"Processando: {caminho_arquivo}")
    
    try:
        # Ajusta o caminho para formato aceito pelo MySQL
        caminho_mysql = caminho_arquivo.replace("\\", "/")

        # Carrega os dados diretamente no MySQL
        cursor.execute(f"""
            LOAD DATA LOCAL INFILE '{caminho_mysql}'
            INTO TABLE empresas
            CHARACTER SET latin1
            FIELDS TERMINATED BY ';'
            OPTIONALLY ENCLOSED BY '"'
            LINES TERMINATED BY '\n'
            IGNORE 0 LINES
        """)
        conn.commit()
        print(f"{nome_arquivo} carregado com sucesso.")

    except Exception as e:
        print(f"Erro ao carregar {nome_arquivo}: {e}")

# Encerra a conexão
cursor.close()
conn.close()

print("Inserção de todos os arquivos de empresas concluída com sucesso!")
