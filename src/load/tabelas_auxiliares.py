import pandas as pd
import os
import time
from src.utils.db_utils import to_sql

def carregar_tabela_simples(arquivos, pasta, engine, nome_tabela):
    print(f'\n##########################\n## Arquivos de {nome_tabela}:\n##########################')
    
    insert_start = time.time()
    
    for arq in arquivos:
        print('Trabalhando no arquivo: ' + arq + ' [...]')
        try:
            del df
        except:
            pass

        df_dtypes = ({0: 'Int32', 1: object})
        path = os.path.join(pasta, arq)
        
        df = pd.read_csv(filepath_or_buffer=path, sep=';', skiprows=0, header=None, dtype=df_dtypes, encoding='latin-1')

        df = df.reset_index()
        del df['index']
        
        df.columns = ['codigo', 'descricao']
        to_sql(df, name=nome_tabela, con=engine, if_exists='append', index=False)
        print('Arquivo ' + arq + ' inserido com sucesso no banco de dados!')

    try:
        del df
    except:
        pass
        
    print(f'Arquivos de {nome_tabela} finalizados!')
    insert_end = time.time()
    tempo_insert = round((insert_end - insert_start))
    print(f'Tempo de execução do processo de {nome_tabela} (em segundos): {tempo_insert}')