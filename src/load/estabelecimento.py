import pandas as pd
import os
import time
import gc
from src.utils.db_utils import to_sql

def carregar_estabelecimento(arquivos, pasta, engine):
    estabelecimento_insert_start = time.time()
    print("""
###############################
## ESTABELECIMENTO files:
###############################
""")

    print(f'There are {len(arquivos)} establishment files!')
    for e in range(0, len(arquivos)):
        print('Working on file: ' + arquivos[e] + ' [...]')
        try:
            del df
            gc.collect()
        except:
            pass

        estabelecimento_dtypes = {
            0: object, 1: object, 2: object, 3: 'Int32', 4: object, 5: 'Int32', 6: 'Int32',
            7: 'Int32', 8: object, 9: object, 10: 'Int32', 11: 'Int32', 12: object, 13: object,
            14: object, 15: object, 16: object, 17: object, 18: object, 19: object,
            20: 'Int32', 21: object, 22: object, 23: object, 24: object, 25: object,
            26: object, 27: object, 28: object, 29: 'Int32'
        }
        extracted_file_path = os.path.join(pasta, arquivos[e])

        NROWS = 2000000
        part = 0
        while True:
            try:
                df = pd.read_csv(
                    filepath_or_buffer=extracted_file_path,
                    sep=';',
                    nrows=NROWS,
                    skiprows=NROWS * part,
                    header=None,
                    dtype=estabelecimento_dtypes,
                    encoding='latin-1',
                )
            except pd.errors.EmptyDataError:
                break

            if df.empty:
                break

            df = df.reset_index()
            del df['index']
            gc.collect()

            df.columns = [
                'basic_cnpj','order_cnpj','cnpj_verification_digit','main_or_branch',
                'name','registration_status_code',
                'registration_status_date',
                'registration_status_reason_code','foreign_city_name','country_code',
                'start_activity_date','primary_cnae_code','secondary_cnae_code',
                'street_type',
                'street_name','number',
                'complement',
                'neigborhood',
                'zip_code'
                ,'state','city_code',
                'area_code_1','phone_1','area_code_2','phone_2','fax_area_code','fax',
                'email',
                'special_status',
                'special_status_date'
            ]

            to_sql(df, name='establishment', con=engine, if_exists='append', index=False)
            print('File ' + arquivos[e] + ' / ' + str(part) + ' successfully inserted into the database!')
            
            if len(df) == NROWS:
                part += 1
            else:
                break

    try:
        del df
        gc.collect()
    except:
        pass
        
    print('ESTABELECIMENTO files finished!')
    estabelecimento_insert_end = time.time()
    estabelecimento_Tempo_insert = round((estabelecimento_insert_end - estabelecimento_insert_start))
    print('Execution time for the ESTABELECIMENTO process (in seconds): ' + str(estabelecimento_Tempo_insert))