import pymysql

# Conectar ao banco
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='receita',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.Cursor
)

cursor = conn.cursor()

# Remove a tabela de destino se já existir
cursor.execute("DROP TABLE IF EXISTS cnt_empresas_por_cnpj8")

# Cria a nova tabela com os mesmos campos da original
cursor.execute("""
CREATE TABLE cnt_empresas_por_cnpj8 AS
SELECT cnpj8,
        count(cnpj_completo) as cnt_empresas
FROM cnpjs_filtrados_em_comum
group by 1
""")

conn.commit()
print("Tabela 'cnt_empresas_por_cnpj8' criada com sucesso com os dados filtrados.")

# Fecha a conexão
cursor.close()
conn.close()
