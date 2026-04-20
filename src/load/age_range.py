import pandas as pd
import time
from src.utils.db_utils import to_sql

def carregar_age_range(engine, nome_tabela):
    print(f'\n## Carregando tabela {nome_tabela}:\n')
    
    insert_start = time.time()
    
    try:
        del df
    except:
        pass
    
    df = pd.DataFrame({
        'codigo': [1, 2, 3, 4, 5, 6, 7, 8, 9, 0],
        'descricao': [
            '0 a 12 anos',
            '13 a 20 anos',
            '21 a 30 anos',
            '31 a 40 anos',
            '41 a 50 anos',
            '51 a 60 anos',
            '61 a 70 anos',
            '71 a 80 anos',
            'Maiores de 80 anos',
            'Não se aplica'
        ]
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
