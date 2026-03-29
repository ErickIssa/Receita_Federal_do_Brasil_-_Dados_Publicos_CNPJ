import pandas as pd
import os
from src.utils.db_utils import to_sql

def carregar_socios(arquivos, pasta, engine):
    for arq in arquivos:
        print(f'Socios: {arq}')
        path = os.path.join(pasta, arq)

        df = pd.read_csv(path, sep=';', header=None, encoding='latin-1')

        df.columns = [
            'cnpj_basico','identificador_socio','nome_socio_razao_social',
            'cpf_cnpj_socio','qualificacao_socio','data_entrada_sociedade',
            'pais','representante_legal','nome_do_representante',
            'qualificacao_representante_legal','faixa_etaria'
        ]

        to_sql(df, name='socios', con=engine, if_exists='append', index=False)