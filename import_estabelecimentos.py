import mysql.connector
import os

# Caminho base e arquivos
diretorio = "C:/Users/User/Documents/Receita Federal/estabelecimentos/"
prefixo = "K3241.K03200Y"
sufixo = ".D50614.ESTABELE"
arquivos = [f"{prefixo}{i}{sufixo}" for i in range(10)]

# Conecta ao banco de dados
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='receita',
    allow_local_infile=True  # Habilita uso de LOAD DATA LOCAL INFILE
)
cursor = conn.cursor()

# Remove a tabela antiga se existir
cursor.execute("DROP TABLE IF EXISTS estabelecimentos")

# Cria a nova tabela
cursor.execute("""
CREATE TABLE estabelecimentos (
    cnpj8 VARCHAR(8),
    cnpj_ordem VARCHAR(4),
    cnpj_dv VARCHAR(2),
    identificador_matriz VARCHAR(1),
    nome_fantasia VARCHAR(255),
    situacao_cadastral VARCHAR(3),
    data_situacao VARCHAR(8),
    motivo_situacao VARCHAR(2),
    nome_cidade_exterior VARCHAR(100),
    pais VARCHAR(3),
    data_inicio_atividade VARCHAR(8),
    cnae_fiscal_principal VARCHAR(7),
    cnae_fiscal_secundario TEXT,
    tipo_logradouro VARCHAR(30),
    logradouro VARCHAR(255),
    numero VARCHAR(20),
    complemento TEXT,
    bairro VARCHAR(100),
    cep VARCHAR(8),
    uf VARCHAR(2),
    municipio VARCHAR(7),
    ddd_1 VARCHAR(5),
    telefone_1 VARCHAR(15),
    ddd_2 VARCHAR(5),
    telefone_2 VARCHAR(15),
    ddd_fax VARCHAR(5),
    fax VARCHAR(15),
    correio_eletronico VARCHAR(255),
    situacao_especial VARCHAR(100),
    data_situacao_especial VARCHAR(8)
)
""")

# Processa os arquivos
for nome_arquivo in arquivos:
    caminho_arquivo = os.path.join(diretorio, nome_arquivo)
    print(f"Processando: {caminho_arquivo}")

    try:
        # Ajusta o caminho para o padrão aceito pelo MySQL (barra normal /)
        caminho_mysql = caminho_arquivo.replace("\\", "/")

        # Executa o comando de carga
        cursor.execute(f"""
            LOAD DATA LOCAL INFILE '{caminho_mysql}'
            INTO TABLE estabelecimentos
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

# Finaliza
cursor.close()
conn.close()
print("Inserção de todos os arquivos concluída com sucesso!")
