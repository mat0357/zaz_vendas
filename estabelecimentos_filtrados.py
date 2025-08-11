import mysql.connector

# Conecta ao banco de dados
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='receita'
)
cursor = conn.cursor()

# Remove a tabela de destino se já existir
cursor.execute("DROP TABLE IF EXISTS estabelecimentos_filtradas")

# Cria a nova tabela com os mesmos campos da original
cursor.execute("""
CREATE TABLE estabelecimentos_filtradas AS
SELECT *
FROM estabelecimentos
WHERE situacao_cadastral = '02'
""")

conn.commit()
print("Tabela 'estabelecimentos_filtradas' criada com sucesso com os dados filtrados.")

# Fecha a conexão
cursor.close()
conn.close()
