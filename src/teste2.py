import sqlite3

def executar_sql_manual():
    conn = sqlite3.connect('cnpjEN.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print("Cole sua query SQL abaixo (digite 'sair' para encerrar):\n")

    query = """
SELECT company.name,
       partner.name,
       age_range.description
FROM company
JOIN partner ON company.basic_cnpj = partner.basic_cnpj
JOIN age_range ON partner.age_range_code = age_range.code
JOIN legal_nature ON company.legal_nature_code = legal_nature.code
WHERE age_range.description = '0 a 12 anos'
  AND legal_nature.description = 'Sociedade Empresária Limitada'
LIMIT 2;
  """
        #query = " select description from legal_nature"

    try:
            cursor.execute(query)

            # Se for SELECT, mostra resultados
            if query.strip().lower().startswith("select"):
                resultados = cursor.fetchall()

                if not resultados:
                    print("⚠️ Nenhum resultado encontrado.")
                else:
                    for i, linha in enumerate(resultados, 1):
                        print(f"{i}: {dict(linha)}")

            else:
                # Para INSERT, UPDATE, DELETE, etc.
                conn.commit()
                print("✅ Query executada com sucesso.")

    except Exception as e:
        print("❌ Erro:", e)

    conn.close()


if __name__ == "__main__":
    executar_sql_manual()