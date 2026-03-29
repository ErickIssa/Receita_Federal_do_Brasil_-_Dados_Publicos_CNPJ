import pandas as pd
import os
from src.utils.db_utils import to_sql

def carregar_empresa(arquivos, pasta, engine):
    for arq in arquivos:
        path = os.path.join(pasta, arq)

        df = pd.read_csv(path, sep=';', header=None, encoding='latin-1')

        df.columns = [
            'basic_cnpj', 'name', 'legal_nature_code',
            'responsible_qualification_code', 'capital',
            'company_size_code', 'responsible_qualification_code'
        ]

        df['capital_social'] = df['capital_social'].str.replace(',', '.').astype(float)

        to_sql(df, name='company', con=engine, if_exists='append', index=False)