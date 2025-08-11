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

print("Criando tabela cnpjs_filtrados_em_comum_simples...")

# Drop se já existir
cursor.execute("DROP TABLE IF EXISTS cnpjs_filtrados_em_comum_simples")

# Cria a nova tabela combinando as duas
cursor.execute("""
    CREATE TABLE cnpjs_filtrados_em_comum_simples AS
    SELECT c.*,
           s.opcao_simples,
           s.data_opcao_simples,
           s.data_exclusao_simples,
           s.opcao_mei,
           s.data_opcao_mei,
           s.data_exclusao_mei
    FROM cnpjs_filtrados_em_comum c
    INNER JOIN simples s
        ON c.cnpj8 = s.cnpj8
""")

conn.commit()
cursor.close()
conn.close()

print("Tabela 'cnpjs_filtrados_em_comum_simples' criada com sucesso!")
