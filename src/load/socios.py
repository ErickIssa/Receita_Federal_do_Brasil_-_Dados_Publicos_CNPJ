import pandas as pd
import os
import time
from src.utils.db_utils import to_sql

def carregar_socios(arquivos, pasta, engine):
    socios_insert_start = time.time()
    print("""
######################
## SOCIOS files:
######################
""")

    for e in range(0, len(arquivos)):
        print('Working on file: ' + arquivos[e] + ' [...]')
        try:
            del df
        except:
            pass

        socios_dtypes = {0: object, 1: 'Int32', 2: object, 3: object, 4: 'Int32', 5: 'Int32', 6: 'Int32',
                         7: object, 8: object, 9: 'Int32', 10: 'Int32'}
        extracted_file_path = os.path.join(pasta, arquivos[e])
        
        df = pd.read_csv(filepath_or_buffer=extracted_file_path,
                         sep=';',
                         skiprows=0,
                         header=None,
                         dtype=socios_dtypes,
                         encoding='latin-1',
        )

        df = df.reset_index()
        del df['index']

        # a coluna "data_entrada_sociedade" não existe no db anterior
        df.columns = [
            'basic_cnpj','partner_type_code','name',
            'cpf_or_cnpj','partner_qualification_code','partnership_entry_date',
            'country_code','legal_representative_cpf','legal_representative_name',
            'legal_representative_qualification_code','age_range_code'
        ]

        to_sql(df, name='partner', con=engine, if_exists='append', index=False)
        print('File ' + arquivos[e] + ' successfully inserted into the database!')

    try:
        del df
    except:
        pass
    
    print('SOCIOS files finished!')
    socios_insert_end = time.time()
    socios_Tempo_insert = round((socios_insert_end - socios_insert_start))
    print('Execution time for the SOCIOS process (in seconds): ' + str(socios_Tempo_insert))