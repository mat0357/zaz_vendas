import pymysql

# Conecta ao banco de dados
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
cursor.execute("DROP TABLE IF EXISTS empresas_filtradas_nat")

# Cria a nova tabela com os mesmos campos da original
cursor.execute("""
CREATE TABLE empresas_filtradas_nat AS
SELECT e.*
FROM empresas e
join simples s on s.cnpj8 = e.cnpj8
WHERE natureza_juridica in ('2038',
'2046',
'2054',
'2062',
'2178',
'2305',
'2313',
'3220')
and s.opcao_simples = 'S'
""")

conn.commit()
print("Tabela 'empresas_filtradas_nat' criada com sucesso com os dados filtrados.")

# Fecha a conexão
cursor.close()
conn.close()
