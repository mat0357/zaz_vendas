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

cursor = conn.cursor()

# Nome da nova tabela combinada
nova_tabela = "dados_combinados_cnpj8"

# 1. Drop tabela se existir
cursor.execute(f"DROP TABLE IF EXISTS {nova_tabela}")

# 2. Criar nova tabela com todos os campos das duas tabelas
cursor.execute(f"""
CREATE TABLE {nova_tabela} (
    -- Campos da cnpjs_filtrados_em_comum_simples
    cnpj8 varchar(8) DEFAULT NULL,
    cnpj_ordem varchar(4) DEFAULT NULL,
    cnpj_dv varchar(2) DEFAULT NULL,
    identificador_matriz varchar(1) DEFAULT NULL,
    nome_fantasia varchar(255) DEFAULT NULL,
    situacao_cadastral varchar(3) DEFAULT NULL,
    data_situacao varchar(8) DEFAULT NULL,
    motivo_situacao varchar(2) DEFAULT NULL,
    nome_cidade_exterior varchar(100) DEFAULT NULL,
    pais varchar(3) DEFAULT NULL,
    data_inicio_atividade varchar(8) DEFAULT NULL,
    cnae_fiscal_principal varchar(7) DEFAULT NULL,
    cnae_fiscal_secundario text,
    tipo_logradouro varchar(30) DEFAULT NULL,
    logradouro varchar(255) DEFAULT NULL,
    numero varchar(20) DEFAULT NULL,
    complemento text,
    bairro varchar(100) DEFAULT NULL,
    cep varchar(8) DEFAULT NULL,
    uf varchar(2) DEFAULT NULL,
    municipio varchar(7) DEFAULT NULL,
    ddd_1 varchar(5) DEFAULT NULL,
    telefone_1 varchar(15) DEFAULT NULL,
    ddd_2 varchar(5) DEFAULT NULL,
    telefone_2 varchar(15) DEFAULT NULL,
    ddd_fax varchar(5) DEFAULT NULL,
    fax varchar(15) DEFAULT NULL,
    correio_eletronico varchar(255) DEFAULT NULL,
    situacao_especial varchar(100) DEFAULT NULL,
    data_situacao_especial varchar(8) DEFAULT NULL,
    cnpj_completo varchar(14) DEFAULT NULL,
    cnpj_formatado varchar(18) DEFAULT NULL,
    opcao_simples varchar(300) DEFAULT NULL,
    data_opcao_simples varchar(300) DEFAULT NULL,
    data_exclusao_simples varchar(300) DEFAULT NULL,
    opcao_mei varchar(300) DEFAULT NULL,
    data_opcao_mei varchar(300) DEFAULT NULL,
    data_exclusao_mei varchar(300) DEFAULT NULL,
    
    -- Campos da empresas_filtradas_nat_simples
    razao_social varchar(255) DEFAULT NULL,
    natureza_juridica varchar(4) DEFAULT NULL,
    qualificacao_responsavel varchar(3) DEFAULT NULL,
    capital_social varchar(20) DEFAULT NULL,
    porte varchar(1) DEFAULT NULL,
    ente_federativo varchar(7) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
""")

# 3. Inserir dados combinados pelo cnpj8
cursor.execute(f"""
INSERT INTO {nova_tabela} (
    cnpj8, cnpj_ordem, cnpj_dv, identificador_matriz, nome_fantasia, situacao_cadastral,
    data_situacao, motivo_situacao, nome_cidade_exterior, pais, data_inicio_atividade,
    cnae_fiscal_principal, cnae_fiscal_secundario, tipo_logradouro, logradouro,
    numero, complemento, bairro, cep, uf, municipio, ddd_1, telefone_1, ddd_2,
    telefone_2, ddd_fax, fax, correio_eletronico, situacao_especial, data_situacao_especial,
    cnpj_completo, cnpj_formatado, opcao_simples, data_opcao_simples, data_exclusao_simples,
    opcao_mei, data_opcao_mei, data_exclusao_mei,
    razao_social, natureza_juridica, qualificacao_responsavel, capital_social,
    porte, ente_federativo
)
SELECT
    c.cnpj8, c.cnpj_ordem, c.cnpj_dv, c.identificador_matriz, c.nome_fantasia, c.situacao_cadastral,
    c.data_situacao, c.motivo_situacao, c.nome_cidade_exterior, c.pais, c.data_inicio_atividade,
    c.cnae_fiscal_principal, c.cnae_fiscal_secundario, c.tipo_logradouro, c.logradouro,
    c.numero, c.complemento, c.bairro, c.cep, c.uf, c.municipio, c.ddd_1, c.telefone_1,
    c.ddd_2, c.telefone_2, c.ddd_fax, c.fax, c.correio_eletronico, c.situacao_especial,
    c.data_situacao_especial, c.cnpj_completo, c.cnpj_formatado, c.opcao_simples,
    c.data_opcao_simples, c.data_exclusao_simples, c.opcao_mei, c.data_opcao_mei,
    c.data_exclusao_mei,
    e.razao_social, e.natureza_juridica, e.qualificacao_responsavel, e.capital_social,
    e.porte, e.ente_federativo
FROM cnpjs_filtrados_em_comum_simples c
INNER JOIN empresas_filtradas_nat_simples e ON c.cnpj8 = e.cnpj8
""")

conn.commit()

print(f"Tabela '{nova_tabela}' criada e populada com sucesso!")

cursor.close()
conn.close()
