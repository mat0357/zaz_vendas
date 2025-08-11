import pymysql
import os

# Caminho completo do arquivo
diretorio = "C:/Users/User/Documents/CCE/Simples"
nome_arquivo = "F.K03200$W.SIMPLES.CSV.D50614"
caminho_arquivo = os.path.join(diretorio, nome_arquivo).replace("\\", "/")

# Conecta ao banco com pymysql
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='receita',
    charset='utf8mb4',
    local_infile=True  # Permite LOAD DATA LOCAL INFILE
)
cursor = conn.cursor()

# Limpa a tabela antes de carregar
print("Apagando dados antigos da tabela 'simples'...")
cursor.execute("DELETE FROM simples")
conn.commit()
print("Dados apagados com sucesso.")

# Carrega o novo CSV
try:
    print(f"Carregando arquivo: {caminho_arquivo}")
    cursor.execute(f"""
        LOAD DATA LOCAL INFILE '{caminho_arquivo}'
        INTO TABLE simples
        CHARACTER SET latin1
        FIELDS TERMINATED BY ';'
        OPTIONALLY ENCLOSED BY '"'
        LINES TERMINATED BY '\n'
        IGNORE 0 LINES
    """)
    conn.commit()
    print("Arquivo carregado com sucesso.")
except Exception as e:
    print(f"Erro ao carregar o arquivo: {e}")

# Finaliza
cursor.close()
conn.close()
print("Processo concluído.")
