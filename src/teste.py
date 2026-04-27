import sqlite3
import os
from datasets import load_dataset


# =========================
# OPÇÃO 1 - EXPLORAR BANCO
# =========================
def explorar_banco():
    conn = sqlite3.connect('cnpj_dados.db')
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tabelas = cursor.fetchall()

    nomes_encontrados = []

    for tabela in tabelas:
        nome_tabela = tabela['name']
        nomes_encontrados.append(nome_tabela)
        
        print(f"\n{'='*20} TABELA: {nome_tabela} {'='*20}")
        
        cursor.execute(f"PRAGMA table_info({nome_tabela});")
        colunas = [col['name'] for col in cursor.fetchall()]
        print(f"COLUNAS: {', '.join(colunas)}")
        print("-" * 50)
        
        try:
            cursor.execute(f"SELECT * FROM {nome_tabela} LIMIT 3;")
            linhas = cursor.fetchall()
            
            if not linhas:
                print(" [Tabela vazia] ")
            else:
                for i, linha in enumerate(linhas, 1):
                    print(f"Registro {i}: {dict(linha)}")

        except sqlite3.Error as e:
            print(f"Erro ao ler dados da tabela {nome_tabela}: {e}")

        print("-" * 50)

    print("\nLISTA DE TABELAS PROCESSADAS:")
    print("\n".join(nomes_encontrados))

    conn.close()


# =========================
# OPÇÃO 2 - TESTAR QUERIES
# =========================
def testar_queries():
    database_path = os.path.join("cnpj_dados.db")
    dataset = load_dataset("ErickIssa/Gemini100questions", split="train")

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    validas = 0
    vazias = 0
    erros = 0

    for i, query in enumerate(dataset['rewritten_sql']):
        if i == 34:
            print(f"\n--- Query {i} PULADA ---")
            continue

        print(f"\n--- Query {i} ---")

        try:
            cursor.execute(query)
            resultado = cursor.fetchone()

            if resultado is None:
                print("⚠️ Consulta vazia")
                vazias += 1
            else:
                print("✅ Retornou resultado")
                validas += 1

        except Exception as e:
            print("❌ Erro:", e)
            erros += 1

    print("\nResumo:")
    print(f"Com resultado: {validas}")
    print(f"Vazias: {vazias}")
    print(f"Erros: {erros}")

    conn.close()


# =========================
# ESCOLHA DO USUÁRIO
# =========================
if __name__ == "__main__":
    print("Escolha uma opção:")
    print("1 - Explorar estrutura do banco")
    print("2 - Testar queries do dataset")

    opcao = input("Digite 1 ou 2: ")

    if opcao == "1":
        explorar_banco()
    elif opcao == "2":
        testar_queries()
    else:
        print("Opção inválida!")