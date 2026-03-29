import sqlite3

# Conecta ao banco de dados mostrado na sua imagem
conn = sqlite3.connect('cnpj_dados.db')
cursor = conn.cursor()

# Pega os nomes de todas as tabelas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tabelas = cursor.fetchall()

print(f"{'TABELA':<25} | {'COLUNA'}")
print("-" * 50)

for tabela in tabelas:
    nome_tabela = tabela[0]
    # Pega informações de cada coluna da tabela
    cursor.execute(f"PRAGMA table_info({nome_tabela});")
    colunas = cursor.fetchall()
    
    for coluna in colunas:
        nome_coluna = coluna[1]
        tipo_coluna = coluna[2]
        print(f"{nome_tabela:<25} | {nome_coluna} ({tipo_coluna})")
    print("-" * 50)

conn.close()