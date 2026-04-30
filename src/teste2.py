import sqlite3

def executar_sql_manual():
    conn = sqlite3.connect('cnpj_dados.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print("Cole sua query SQL abaixo (digite 'sair' para encerrar):\n")

    while True:
        query = input("SQL> ")

        if query.lower() == "sair":
            break

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