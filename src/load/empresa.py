import pandas as pd
import os
from src.utils.db_utils import to_sql

def carregar_empresa(arquivos, pasta, engine):
    for arq in arquivos:
        path = os.path.join(pasta, arq)

        df = pd.read_csv(path, sep=';', header=None, encoding='latin-1')

        df.columns = [
            'cnpj_basico', 'razao_social', 'natureza_juridica',
            'qualificacao_responsavel', 'capital_social',
            'porte_empresa', 'ente_federativo_responsavel'
        ]

        df['capital_social'] = df['capital_social'].str.replace(',', '.').astype(float)

        to_sql(df, name='empresa', con=engine, if_exists='append', index=False)