import pandas as pd
import os
from src.utils.db_utils import to_sql

def carregar_estabelecimento(arquivos, pasta, engine):
    NROWS = 2_000_000

    for arq in arquivos:
        print(f'Estabelecimento: {arq}')
        path = os.path.join(pasta, arq)

        part = 0

        #pra não estourar a memória
        while True:
            df = pd.read_csv(
                path,
                sep=';',
                header=None,
                encoding='latin-1',
                nrows=NROWS,
                skiprows=NROWS * part
            )

            if df.empty:
                break
            #alguns dados de establishment não tem correspondencia
            df.columns = [
                'basic_cnpj','order_cnpj','cnpj_verification_digit','main_or_branch',
                'name','registration_status_code',
                'data_situacao_cadastral',
                'registration_status_reason_code','foreign_city_name','country_code',
                'start_activity_date','primary_cnae_code','secondary_cnae_code',
                'tipo_logradouro',
                'logradouro','numero',
                'complemento',
                'bairro',
                'cep'
                ,'state','city_code',
                'ddd_1','telefone_1','ddd_2','telefone_2','ddd_fax','fax',
                'correio_eletronico',
                'special_status',
                'data_situacao_especial'
            ]

            to_sql(df, name='establishment', con=engine, if_exists='append', index=False)

            part += 1