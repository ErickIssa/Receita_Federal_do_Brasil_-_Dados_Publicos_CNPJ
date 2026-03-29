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

    # 📁 Criar pastas
    makedirs(OUTPUT_FILES)
    makedirs(EXTRACTED_FILES)

    # 🌐 Buscar diretórios disponíveis
    print("Listando diretórios...")
    dirs = listar_diretorios(BASE_URL)

    dir_escolhido = dirs[-1]  # mais antigo (igual seu código original)
    print(f"Diretório escolhido: {dir_escolhido}")

    # 📦 Listar arquivos
    arquivos = listar_arquivos_zip(BASE_URL, dir_escolhido)

    print(f"\nTotal de arquivos: {len(arquivos)}")

    # ⬇️ Download
    print("\n=== DOWNLOAD ===")
    for url in arquivos:
        baixar_arquivo(url, OUTPUT_FILES)

    # 📂 Extração
    print("\n=== EXTRAÇÃO ===")
    for url in arquivos:
        nome = url.split('/')[-1]
        caminho_zip = f"{OUTPUT_FILES}/{nome}"

        try:
            extrair_zip(caminho_zip, EXTRACTED_FILES)
            print(f"[OK] Extraído: {nome}")
        except Exception as e:
            print(f"[ERRO] {nome} -> {e}")

    # 🔀 Separar arquivos
    print("\n=== SEPARANDO ARQUIVOS ===")
    grupos = separar_arquivos(EXTRACTED_FILES)

    for k, v in grupos.items():
        print(f"{k}: {len(v)} arquivos")

    # 🗄️ Banco de dados
    print("\n=== CONECTANDO AO BANCO ===")
    engine = create_engine(f"sqlite:///{DATABASE}")
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    # 🔥 DROP tabelas (igual seu código original)
    print("\n=== LIMPANDO TABELAS ===")
    cur.executescript("""
    DROP TABLE IF EXISTS empresa;
    DROP TABLE IF EXISTS estabelecimento;
    DROP TABLE IF EXISTS socios;
    DROP TABLE IF EXISTS simples;
    DROP TABLE IF EXISTS cnae;
    DROP TABLE IF EXISTS moti;
    DROP TABLE IF EXISTS munic;
    DROP TABLE IF EXISTS natju;
    DROP TABLE IF EXISTS pais;
    DROP TABLE IF EXISTS quals;
    """)
    conn.commit()

    # 🚀 LOAD
    print("\n=== INICIANDO CARGA ===\n")

    inicio = time.time()

    carregar_empresa(grupos["empresa"], EXTRACTED_FILES, engine)
    carregar_estabelecimento(grupos["estabelecimento"], EXTRACTED_FILES, engine)
    carregar_socios(grupos["socios"], EXTRACTED_FILES, engine)
    carregar_simples(grupos["simples"], EXTRACTED_FILES, engine)

    # tabelas auxiliares
    carregar_tabela_simples(grupos["cnae"], EXTRACTED_FILES, engine, "cnae")
    carregar_tabela_simples(grupos["moti"], EXTRACTED_FILES, engine, "moti")
    carregar_tabela_simples(grupos["munic"], EXTRACTED_FILES, engine, "munic")
    carregar_tabela_simples(grupos["natju"], EXTRACTED_FILES, engine, "natju")
    carregar_tabela_simples(grupos["pais"], EXTRACTED_FILES, engine, "pais")
    carregar_tabela_simples(grupos["quals"], EXTRACTED_FILES, engine, "quals")

    fim = time.time()
    print(f"\nTempo de carga: {round(fim - inicio)} segundos")

    # Índices
    print("\n=== CRIANDO ÍNDICES ===")
    cur.executescript("""
    CREATE INDEX IF NOT EXISTS idx_empresa_cnpj ON empresa(cnpj_basico);
    CREATE INDEX IF NOT EXISTS idx_estabelecimento_cnpj ON estabelecimento(cnpj_basico);
    CREATE INDEX IF NOT EXISTS idx_socios_cnpj ON socios(cnpj_basico);
    CREATE INDEX IF NOT EXISTS idx_simples_cnpj ON simples(cnpj_basico);
    """)
    conn.commit()

    print("\nÍndices criados com sucesso!")

    # 🏁 Final
    fim_total = time.time()

    print("\n====================================")
    print("PROCESSO FINALIZADO COM SUCESSO 🚀")
    print("====================================")
    print(f"Tempo total: {round(fim_total - inicio_total)} segundos")

    conn.close()


if __name__ == "__main__":
    main()