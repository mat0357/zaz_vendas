import pymysql

print("Conectando ao banco...")

# Conexão com o banco
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='receita',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.Cursor
)

cursor = conn.cursor()

# Criar nova tabela com empresas da empresas_filtradas_nat que também estão na simples
cursor.execute("""
CREATE TABLE IF NOT EXISTS empresas_filtradas_nat_simples AS
SELECT e.cnpj8,
       e.razao_social,
       e.natureza_juridica,
       e.qualificacao_responsavel,
       e.capital_social,
       e.porte,
       e.ente_federativo
FROM empresas_filtradas_nat e
INNER JOIN simples s
    ON e.cnpj8 = s.cnpj8;
""")

conn.commit()
cursor.close()
conn.close()

print("Tabela 'empresas_filtradas_nat_simples' criada com sucesso!")
