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
cursor.execute("DROP TABLE IF EXISTS municipios_ufs")

# Cria a nova tabela com base na CTE e no join
cursor.execute("""
CREATE TABLE municipios_ufs AS
WITH cidades_ufs AS (
    SELECT DISTINCT
        e.municipio,
        e.uf
    FROM estabelecimentos e
)
SELECT 
    cs.municipio,
    cs.uf,
    m.codigo,
    m.descricao as nome_municipio
FROM cidades_ufs cs 
JOIN municipios m ON m.codigo = cs.municipio
""")

conn.commit()
print("Tabela 'municipios_ufs' criada com sucesso com os dados combinados.")

# Fecha a conexão
cursor.close()
conn.close()
