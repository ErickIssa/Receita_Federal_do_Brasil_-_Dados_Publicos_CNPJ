import sqlite3
import pandas as pd
import os

# =========================
# CONFIG (mesma pasta)
# =========================
DATABASE_NAME = "cnpj_dados.db"
EXCEL_NAME = "perguntas_cnpj.xlsx"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

database_path = DATABASE_NAME
excel_path = EXCEL_NAME


# =========================
# CRIAR DICIONÁRIO {id: query}
# =========================
def criar_dicionario_queries(df, ids):
    dicionario = {}

    for _, row in df.iterrows():
        question_id = row.iloc[1]   # Coluna B
        query = row.iloc[5]         # Coluna F

        if question_id in ids:
            dicionario[question_id] = query

    return dicionario


# =========================
# TESTAR QUERIES (SEM PRINT DE DADOS)
# =========================
def testar_queries(database_path, queries_dict):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    for qid, query in queries_dict.items():
        print(f"\nID {qid}:", end=" ")

        # Query vazia
        if pd.isna(query) or str(query).strip() == "":
            print("⚠️ VAZIA")
            continue

        try:
            cursor.execute(query)

            # pega só 1 linha (mais eficiente)
            resultado = cursor.fetchone()

            if resultado:
                print("✅ OK")
            else:
                print("⚠️ SEM RESULTADO")

        except Exception:
            print("❌ ERRO")

    conn.close()


# =========================
# IDS PROBLEMA
# =========================
ids_problema = [
    129
]


# =========================
# EXECUÇÃO DIRETA
# =========================
if __name__ == "__main__":
    df = pd.read_excel(excel_path)

    queries_dict = criar_dicionario_queries(df, ids_problema)

    print(f"Testando {len(queries_dict)} queries...\n")

    testar_queries(database_path, queries_dict)