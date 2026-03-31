import pandas as pd
import os
from src.utils.db_utils import to_sql

#O simples é a taxação/taxation
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
                'basic_cnpj','option_for_simples_taxation','simples_taxation_option_date',
                'simples_taxation_exclusion_date','option_for_mei_taxation','mei_taxation_option_date','mei_taxation_exclusion_date'
            ]

            to_sql(df, name='taxation', con=engine, if_exists='append', index=False)