import pymysql

print("Conectando ao banco...")

# Configuração da conexão
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='receita',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.Cursor
)

print("Conectado ao banco...")

cursor = conn.cursor()

# Remove tabela antiga, se existir
cursor.execute("DROP TABLE IF EXISTS receita.tabela_fit_matriz;")

# Query corrigida
query = """
CREATE TABLE receita.tabela_fit_matriz AS
WITH

primeiro_fit AS (
  SELECT
    *,
    CASE
      WHEN cn.caracteristica = 'Alto consumo' AND cn.Manual = 'Baixo Consumo' THEN 5
      WHEN cn.caracteristica = 'Alto consumo' AND cn.Manual = 'Médio Consumo' THEN 4
      WHEN cn.caracteristica = 'Alto consumo' AND cn.Manual = 'Alto Consumo' THEN 3
      WHEN cn.caracteristica = 'Verificar' AND cn.Manual = 'Baixo Consumo' THEN 5
      WHEN cn.caracteristica = 'Verificar' AND cn.Manual = 'Médio Consumo' THEN 4
      WHEN cn.caracteristica = 'Verificar' AND cn.Manual = 'Alto Consumo' THEN 3
    END AS compatibilidade
  FROM receita.dados_combinados_cnpj8 c
  JOIN receita.classificação_manual_cnae cn 
    ON cn.codigo = c.cnae_fiscal_principal
),

-- Conversão de capital_social para número
segundo_fit AS (
  SELECT 
    pf.*,
    (YEAR(CURRENT_DATE()) - SUBSTR(data_inicio_atividade, 1, 4)) AS tempo_de_vida,
    CAST(REPLACE(capital_social, ',', '.') AS DECIMAL(15,2)) AS capital_social_num,
    CASE
      WHEN CAST(REPLACE(capital_social, ',', '.') AS DECIMAL(15,2)) BETWEEN 0 AND 100000 THEN 5
      WHEN CAST(REPLACE(capital_social, ',', '.') AS DECIMAL(15,2)) BETWEEN 100000 AND 500000 THEN 4
      WHEN CAST(REPLACE(capital_social, ',', '.') AS DECIMAL(15,2)) BETWEEN 500000 AND 1000000 THEN 3
      WHEN CAST(REPLACE(capital_social, ',', '.') AS DECIMAL(15,2)) > 1000000 THEN 2
    END AS capital_inicial,
    cn.cnt_empresas
  FROM primeiro_fit pf
  LEFT JOIN receita.cnt_empresas_por_cnpj8 cn 
    ON cn.cnpj8 = pf.cnpj8
),

terceiro_fit AS (
  SELECT 
    sf.*,
    CASE
      WHEN tempo_de_vida BETWEEN 0 AND 2 THEN 5
      WHEN tempo_de_vida BETWEEN 2 AND 10 THEN 4
      WHEN tempo_de_vida BETWEEN 10 AND 30 THEN 3
      WHEN tempo_de_vida > 30 THEN 2
    END AS classificacao_vida,
    CASE
      WHEN sf.cnt_empresas BETWEEN 1 AND 3 THEN 2
      WHEN sf.cnt_empresas BETWEEN 3 AND 5 THEN 3
      WHEN sf.cnt_empresas BETWEEN 5 AND 10 THEN 4
      WHEN sf.cnt_empresas > 10 THEN 5
    END AS num_filiais,  
    dmu.distribuidora
  FROM segundo_fit sf
  LEFT JOIN receita.distribuidora_municipio_uf dmu 
    ON sf.municipio = dmu.codigo
  WHERE dmu.distribuidora IN (
    'Cemig-D', 'Equatorial PA', 'Neoenergia Coelba', 'Equatorial MA',
    'Enel CE', 'Neoenergia Cosern', 'Energisa AC', 'Enel GO',
    'Energisa Sul-Sudeste', 'Neoenergia Pernambuco', 'EDP ES', 'Copel-Dis',
    'Energisa MT', 'Energisa MS', 'Celesc-Dis', 'Light',
    'Neoenergia Elektro', 'Neoenergia Brasilia', 'CPFL Paulista',
    'Energisa Minas Rio', 'EDP SP', 'Energisa RO', 'Energisa TO',
    'Energisa PB', 'Equatorial PI', 'Amazonas Energia', 'CEEE Equatorial',
    'CEA Equatorial', 'Energisa SE', 'Equatorial AL'
  )
  and identificador_matriz = 1
)

SELECT 
  *,
  (classificacao_vida + capital_inicial + compatibilidade + num_filiais) AS score_prospeccao
FROM terceiro_fit;
"""

cursor.execute(query)
conn.commit()

print("Tabela criada com sucesso!")

cursor.close()
conn.close()