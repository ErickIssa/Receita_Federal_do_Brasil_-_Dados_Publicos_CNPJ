import pandas as pd
import os
from src.utils.db_utils import to_sql

def carregar_simples(arquivos, pasta, engine):
    for arq in arquivos:
        print(f'Simples: {arq}')
        path = os.path.join(pasta, arq)

        tamanho = sum(1 for _ in open(path, "r"))
        chunk = 1_000_000

        for i in range(0, tamanho, chunk):
            df = pd.read_csv(
                path,
                sep=';',
                header=None,
                encoding='latin-1',
                skiprows=i,
                nrows=chunk
            )

            df.columns = [
                'cnpj_basico','opcao_pelo_simples','data_opcao_simples',
                'data_exclusao_simples','opcao_mei','data_opcao_mei','data_exclusao_mei'
            ]

            to_sql(df, name='simples', con=engine, if_exists='append', index=False)