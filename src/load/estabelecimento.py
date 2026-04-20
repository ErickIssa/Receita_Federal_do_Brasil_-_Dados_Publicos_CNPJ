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

            df.columns = ['cnpj_basico',
                                   'cnpj_ordem',
                                   'cnpj_digito_verificador',
                                   'matriz_ou_filial',
                                   'nome',
                                   'codigo_situacao_cadastral',
                                   'data_situacao_cadastral',
                                   'codigo_motivo_situacao_cadastral',
                                   'nome_cidade_estrangeira',
                                   'codigo_pais',
                                   'data_inicio_atividade',
                                   'codigo_cnae_principal',
                                   'codigo_cnae_secundaria',
                                   'tipo_logradouro',
                                   'logradouro',
                                   'numero',
                                   'complemento',
                                   'bairro',
                                   'cep',
                                   'estado',
                                   'codigo_cidade',
                                   'ddd_1',
                                   'telefone_1',
                                   'ddd_2',
                                   'telefone_2',
                                   'ddd_fax',
                                   'fax',
                                   'correio_eletronico',
                                   'situacao_especial',
                                   'data_situacao_especial']
            
            #Colunas: cnpj_basico, cnpj_ordem, cnpj_digito_verificador, matriz_ou_filial, nome, 
            # data_inicio_atividade, codigo_cnae_principal, codigo_cnae_secundaria, 
            # codigo_cidade, estado, codigo_pais, nome_cidade_estrangeira, 
            # situacao_especial, codigo_situacao_cadastral, codigo_motivo_situacao_cadastral

            to_sql(df, name='estabelecimento', con=engine, if_exists='append', index=False)
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