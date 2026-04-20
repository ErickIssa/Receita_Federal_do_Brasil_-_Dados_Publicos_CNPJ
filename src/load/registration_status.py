import pandas as pd
import time
from src.utils.db_utils import to_sql

def carregar_registration_status(engine, nome_tabela):
    print(f'\n## Carregando tabela {nome_tabela}:\n')
    
    insert_start = time.time()
    
    try:
        del df
    except:
        pass
    
    #mantenho em ingles?
    df = pd.DataFrame({
        'codigo': [1, 2, 3, 4, 8],
        'descricao': ['NULA', 'ATIVA', 'SUSPENSA', 'INAPTA', 'BAIXADA']
    })
    
    df = df.astype({'codigo': 'Int32', 'descricao': object})
    
    to_sql(df, name=nome_tabela, con=engine, if_exists='append', index=False)
    print(f'Tabela {nome_tabela} populada com sucesso no banco de dados!')

    try:
        del df
    except:
        pass
        
    print(f'Processo de {nome_tabela} finalizado!')
    insert_end = time.time()
    tempo_insert = round((insert_end - insert_start))
    print(f'Tempo de execução do processo de {nome_tabela} (em segundos): {tempo_insert}')
