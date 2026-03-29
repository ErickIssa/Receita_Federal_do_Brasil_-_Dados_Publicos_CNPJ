import pandas as pd
import os
from src.utils.db_utils import to_sql

def carregar_tabela_simples(arquivos, pasta, engine, nome_tabela):
    for arq in arquivos:
        print(f'{nome_tabela}: {arq}')
        path = os.path.join(pasta, arq)

        df = pd.read_csv(path, sep=';', header=None, encoding='latin-1')

        df.columns = ['codigo', 'descricao']

        to_sql(df, name=nome_tabela, con=engine, if_exists='append', index=False)