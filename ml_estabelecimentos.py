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

print("Criando tabela estabelecimentos_ml...")

# Drop tabela antiga
cursor.execute("DROP TABLE IF EXISTS estabelecimentos_ml")

# Criação da nova tabela
cursor.execute("""
    CREATE TABLE estabelecimentos_ml (
        _id VARCHAR(50),
        mes_referencia VARCHAR(6),
        cod_perf_agente VARCHAR(20),
        sigla_perfil_agente VARCHAR(50),
        nome_empresarial VARCHAR(255),
        cod_parcela_carga VARCHAR(50),
        sigla_parcela_carga VARCHAR(50),
        cnpj_carga VARCHAR(14),
        cidade VARCHAR(100),
        estado_uf VARCHAR(2),
        ramo_atividade VARCHAR(255),
        submercado VARCHAR(50),
        data_migracao TEXT,
        cod_perf_agente_conectado VARCHAR(20),
        sigla_perfil_agente_conectado VARCHAR(50),
        capacidade_carga VARCHAR(50),
        consumo_acl VARCHAR(50),
        consumo_cativo_parc_livre VARCHAR(50),
        consumo_total VARCHAR(50),
        cnpj8 VARCHAR(8),
        razao_social VARCHAR(255),
        natureza_juridica VARCHAR(255),
        qualificacao_responsavel VARCHAR(255),
        capital_social VARCHAR(50),
        porte VARCHAR(50),
        ente_federativo VARCHAR(100),
        valor_pot DECIMAL(18, 2),
        identificador_matriz VARCHAR(1),
        nome_fantasia VARCHAR(255),
        situacao_cadastral INT,
        data_situacao TEXT,
        motivo_situacao INT,
        nome_cidade_exterior VARCHAR(255),
        pais VARCHAR(100),
        data_inicio_atividade TEXT,
        cnae_fiscal_principal VARCHAR(7),
        cnae_fiscal_secundario TEXT,
        tipo_logradouro VARCHAR(50),
        logradouro VARCHAR(255),
        numero VARCHAR(20),
        complemento VARCHAR(250),
        bairro VARCHAR(150),
        cep VARCHAR(10),
        uf VARCHAR(2),
        municipio VARCHAR(250),
        descricao VARCHAR(255)
    )
""")

conn.commit()

print("Inserindo dados...")

cursor.execute("""
    INSERT INTO estabelecimentos_ml (
        _id, mes_referencia, cod_perf_agente, sigla_perfil_agente,
        nome_empresarial, cod_parcela_carga, sigla_parcela_carga, cnpj_carga,
        cidade, estado_uf, ramo_atividade, submercado, data_migracao,
        cod_perf_agente_conectado, sigla_perfil_agente_conectado,
        capacidade_carga, consumo_acl, consumo_cativo_parc_livre,
        consumo_total, cnpj8, razao_social, natureza_juridica,
        qualificacao_responsavel, capital_social, porte, ente_federativo,
        valor_pot, identificador_matriz, nome_fantasia, situacao_cadastral,
        data_situacao, motivo_situacao, nome_cidade_exterior, pais,
        data_inicio_atividade, cnae_fiscal_principal, cnae_fiscal_secundario,
        tipo_logradouro, logradouro, numero, complemento, bairro, cep,
        uf, municipio, descricao
    )
    SELECT
        ml._id,
        ml.mes_referencia,
        ml.cod_perf_agente,
        ml.sigla_perfil_agente,
        ml.nome_empresarial,
        ml.cod_parcela_carga,
        ml.sigla_parcela_carga,
        ml.cnpj_carga,
        ml.cidade,
        ml.estado_uf,
        ml.ramo_atividade,
        ml.submercado,
        ml.data_migracao,
        ml.cod_perf_agente_conectado,
        ml.sigla_perfil_agente_conectado,
        ml.capacidade_carga,
        ml.consumo_acl,
        ml.consumo_cativo_parc_livre,
        ml.consumo_total,
        ml.cnpj8,
        ml.razao_social,
        ml.natureza_juridica,
        ml.qualificacao_responsavel,
        ml.capital_social,
        ml.porte,
        ml.ente_federativo,
        ROUND(
            (REPLACE(ml.capital_social, ',', '.') + 0) /
            NULLIF((REPLACE(ml.consumo_total, ',', '.') + 0), 0), 2
        ) AS valor_pot,
        e.identificador_matriz,
        e.nome_fantasia,
        e.situacao_cadastral,
        e.data_situacao,
        e.motivo_situacao,
        e.nome_cidade_exterior,
        e.pais,
        e.data_inicio_atividade,
        e.cnae_fiscal_principal,
        e.cnae_fiscal_secundario,
        e.tipo_logradouro,
        e.logradouro,
        e.numero,
        e.complemento,
        e.bairro,
        e.cep,
        e.uf,
        e.municipio,
        c.descricao
    FROM receita.ml_com_receita ml
    JOIN receita.estabelecimentos_filtradas e ON e.cnpj_completo = ml.cnpj_carga
    JOIN receita.cnae c ON c.codigo = e.cnae_fiscal_principal
""")

conn.commit()
cursor.close()
conn.close()

print("Tabela 'estabelecimentos_ml' criada com sucesso!")
