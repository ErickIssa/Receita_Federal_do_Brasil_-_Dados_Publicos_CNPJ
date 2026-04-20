import pandas as pd
import os
import time
from src.utils.db_utils import to_sql

def carregar_empresa(arquivos, pasta, engine):
    empresa_insert_start = time.time()
    print("""
#######################
## EMPRESA files:
#######################
""")

    for e in range(0, len(arquivos)):
        print('Working on file: ' + arquivos[e] + ' [...]')
        try:
            del df
        except:
            pass

        empresa_dtypes = {0: object, 1: object, 2: 'Int32', 3: 'Int32', 4: object, 5: 'Int32', 6: object}
        extracted_file_path = os.path.join(pasta, arquivos[e])

        df = pd.read_csv(filepath_or_buffer=extracted_file_path,
                         sep=';',
                         skiprows=0,
                         header=None,
                         dtype=empresa_dtypes,
                         encoding='latin-1',
        )

        df = df.reset_index()
        del df['index']

  
        df.columns = ['cnpj_basico', 'nome', 'codigo_natureza_juridica', 'codigo_qualificacao_responsavel', 
         'capital', 'codigo_porte_empresa', 'ente_federativo_responsavel']

        df['capital'] = df['capital'].apply(lambda x: str(x).replace(',', '.') if isinstance(x, str) else x)
        df['capital'] = df['capital'].astype(float)

        to_sql(df, name='empresa', con=engine, if_exists='append', index=False)
        print('File ' + arquivos[e] + ' successfully inserted into the database!')

    try:
        del df
    except:
        pass
    
    print('EMPRESA files finished!')
    empresa_insert_end = time.time()
    empresa_Tempo_insert = round((empresa_insert_end - empresa_insert_start))
    print('Execution time for the EMPRESA process (in seconds): ' + str(empresa_Tempo_insert))