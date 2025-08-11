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

print("Criando tabela ml_com_receita...")

# Drop se já existir
cursor.execute("DROP TABLE IF EXISTS ml_com_receita")

# Cria a nova tabela com base no JOIN
cursor.execute("""
    CREATE TABLE ml_com_receita AS
    SELECT 
        bm.*,
        ef.*
    FROM empresas_filtradas ef
    JOIN base_ml bm ON LEFT(bm.cnpj_carga, 8) = ef.cnpj8
""")

conn.commit()
cursor.close()
conn.close()

print("Tabela 'ml_com_receita' criada com sucesso!")
