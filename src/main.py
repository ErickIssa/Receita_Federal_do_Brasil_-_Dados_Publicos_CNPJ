import os
import sys

# Adiciona a pasta raiz (uma acima de src) ao path do Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
import sqlite3
import time

from src.config import *

from src.utils.file_utils import makedirs
from src.download.webdav import listar_diretorios, listar_arquivos_zip
from src.download.downloader import baixar_arquivo
from src.extract.extractor import extrair_zip
from src.transform.separar_arquivos import separar_arquivos

from src.load.empresa import carregar_empresa
from src.load.estabelecimento import carregar_estabelecimento
from src.load.socios import carregar_socios
from src.load.simples import carregar_simples
from src.load.tabelas_auxiliares import carregar_tabela_simples


def main():
    inicio_total = time.time()

    print("\n=== INICIANDO PROCESSO ===\n")

    print("Escolha o modo de execução:")
    print("1 - Baixar novos dados e extrair (Processo completo)")
    print("2 - Apenas extrair arquivos ZIP já presentes na pasta 'output_files'")
    print("3 - Usar dados já extraídos na pasta 'extracted_files' (ir direto para o banco de dados)")
    while True:
        opcao = input("Digite a opção (1, 2 ou 3): ").strip()
        if opcao in ['1', '2', '3']:
            break
        print("Opção inválida. Digite 1, 2 ou 3.")

    makedirs(OUTPUT_FILES)
    makedirs(EXTRACTED_FILES)

    if opcao in ['1', '2']:
        if opcao == '1':
            print("Listando diretórios...")
            dirs = listar_diretorios(BASE_URL)

            dir_escolhido = dirs[-1]  # mais antigo
            print(f"Diretório escolhido: {dir_escolhido}")

            arquivos = listar_arquivos_zip(BASE_URL, dir_escolhido)

            print(f"\nTotal de arquivos: {len(arquivos)}")

            print("\n=== DOWNLOAD ===")
            for url in arquivos:
                baixar_arquivo(url, OUTPUT_FILES)
            
            arquivos_para_extrair = [url.split('/')[-1] for url in arquivos]
            
        else: # opcao 2
            arquivos_para_extrair = [f for f in os.listdir(OUTPUT_FILES) if f.endswith('.zip')]
            print(f"\nTotal de arquivos ZIP encontrardos localmente: {len(arquivos_para_extrair)}")

        print("\n=== EXTRAÇÃO ===")
        for nome in arquivos_para_extrair:
            caminho_zip = f"{OUTPUT_FILES}/{nome}"

            try:
                extrair_zip(caminho_zip, EXTRACTED_FILES)
                print(f"[OK] Extraído: {nome}")
            except Exception as e:
                print(f"[ERRO] {nome} -> {e}")

    print("\n=== SEPARANDO ARQUIVOS ===")
    grupos = separar_arquivos(EXTRACTED_FILES)

    for k, v in grupos.items():
        print(f"{k}: {len(v)} arquivos")

    print("\n=== CONECTANDO AO BANCO ===")
    engine = create_engine(f"sqlite:///{DATABASE}")
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    print("\n=== LIMPANDO TABELAS ===")
    cur.executescript("""
    DROP TABLE IF EXISTS company;
    DROP TABLE IF EXISTS establishment;
    DROP TABLE IF EXISTS partner;
    DROP TABLE IF EXISTS taxation;
    DROP TABLE IF EXISTS cnae;
    DROP TABLE IF EXISTS moti;
    DROP TABLE IF EXISTS munic;
    DROP TABLE IF EXISTS natju;
    DROP TABLE IF EXISTS pais;
    DROP TABLE IF EXISTS quals;
    """)
    conn.commit()

    print("\n=== INICIANDO CARGA ===\n")

    inicio = time.time()

    carregar_empresa(grupos["empresa"], EXTRACTED_FILES, engine)
    carregar_estabelecimento(grupos["estabelecimento"], EXTRACTED_FILES, engine)
    carregar_socios(grupos["socios"], EXTRACTED_FILES, engine)
    carregar_simples(grupos["simples"], EXTRACTED_FILES, engine)

    # tabelas auxiliares (tem que modficar a funcao dps)
    carregar_tabela_simples(grupos["cnae"], EXTRACTED_FILES, engine, "cnae")
    carregar_tabela_simples(grupos["moti"], EXTRACTED_FILES, engine, "moti")
    carregar_tabela_simples(grupos["munic"], EXTRACTED_FILES, engine, "munic")
    carregar_tabela_simples(grupos["natju"], EXTRACTED_FILES, engine, "natju")
    carregar_tabela_simples(grupos["pais"], EXTRACTED_FILES, engine, "pais")
    carregar_tabela_simples(grupos["quals"], EXTRACTED_FILES, engine, "quals")

    fim = time.time()
    print(f"\nTempo de carga: {round(fim - inicio)} segundos")



    fim_total = time.time()

    print("\n====================================")
    print("PROCESSO FINALIZADO COM SUCESSO ")
    print("====================================")
    print(f"Tempo total: {round(fim_total - inicio_total)} segundos")

    conn.close()


if __name__ == "__main__":
    main()