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

print("Criando tabela cnpjs_filtrados_em_comum...")

# Drop se já existir
cursor.execute("DROP TABLE IF EXISTS cnpjs_filtrados_em_comum")

# Cria a nova tabela com base no filtro de cnpj8
cursor.execute("""
    CREATE TABLE cnpjs_filtrados_em_comum AS
    SELECT *
    FROM estabelecimentos_filtradas
    WHERE cnpj8 IN (SELECT DISTINCT cnpj8 FROM empresas_filtradas_nat)
""")

conn.commit()
cursor.close()
conn.close()

print("Tabela 'cnpjs_filtrados_em_comum' criada com sucesso!")
