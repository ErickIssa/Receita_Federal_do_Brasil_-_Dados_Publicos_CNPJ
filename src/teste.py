import sqlite3

# Conecta ao banco de dados
conn = sqlite3.connect('cnpj_dados.db')
conn.row_factory = sqlite3.Row 
cursor = conn.cursor()

# Pega os nomes de todas as tabelas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tabelas = cursor.fetchall()

for tabela in tabelas:
    nome_tabela = tabela['name']
    
    # ALTERAÇÃO AQUI: Usei aspas simples no '=' para não conflitar com as aspas da f-string
    print(f"\n{'='*20} TABELA: {nome_tabela} {'='*20}")
    
    # 1. Print da Estrutura (Colunas)
    cursor.execute(f"PRAGMA table_info({nome_tabela});")
    colunas = [col['name'] for col in cursor.fetchall()]
    print(f"COLUNAS: {', '.join(colunas)}")
    print("-" * 50)
    
    # 2. Print de Amostra de Dados
    try:
        cursor.execute(f"SELECT * FROM {nome_tabela} LIMIT 3;")
        linhas = cursor.fetchall()
        
        if not linhas:
            print(" [Tabela vazia] ")
        else:
            for i, linha in enumerate(linhas, 1):
                dados_formatados = dict(linha)
                print(f"Registro {i}: {dados_formatados}")
    except sqlite3.Error as e:
        print(f"Erro ao ler dados da tabela {nome_tabela}: {e}")

    print("-" * 50)

conn.close()