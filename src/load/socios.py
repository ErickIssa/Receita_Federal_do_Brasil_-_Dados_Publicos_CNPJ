import pandas as pd
import os
from src.utils.db_utils import to_sql

def carregar_socios(arquivos, pasta, engine):
    for arq in arquivos:
        print(f'Socios: {arq}')
        path = os.path.join(pasta, arq)

        df = pd.read_csv(path, sep=';', header=None, encoding='latin-1')

        #a coluna "data_entrada_sociedade" não existe no db anterior
        df.columns = [
            'basic_cnpj','partner_type_code','name',
            'cpf_or_cnpj','partner_qualification_code','data_entrada_sociedade',
            'country_code','legal_representative_cpf','legal_representative_name',
            'legal_representative_qualification_code','age_range_code'
        ]

        to_sql(df, name='partner', con=engine, if_exists='append', index=False)