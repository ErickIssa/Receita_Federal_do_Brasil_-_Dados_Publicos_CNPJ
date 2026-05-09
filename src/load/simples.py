import pandas as pd
import os
import time
import math
from sqlalchemy import text
from src.utils.db_utils import to_sql

#O simples é a taxação/taxation
def carregar_simples(arquivos_simples, extracted_files, engine):
    print("""
################################
## Arquivos do SIMPLES NACIONAL:
################################
""")

    # O DROP TABLE agora é feito centralizadamente no main.py

    simples_insert_start = time.time()

    for e in range(0, len(arquivos_simples)):
        print('Trabalhando no arquivo: '+arquivos_simples[e]+' [...]')
        try:
            del simples
        except:
            pass

        print('Lendo o arquivo ' + arquivos_simples[e]+' [...]')
        simples_dtypes = ({0: object, 1: object, 2: 'Int32', 3: 'Int32', 4: object, 5: 'Int32', 6: 'Int32'})
        extracted_file_path = os.path.join(extracted_files, arquivos_simples[e])

        simples_lenght = sum(1 for line in open(extracted_file_path, "r"))
        print('Linhas no arquivo do Simples '+ arquivos_simples[e] +': '+str(simples_lenght))

        tamanho_das_partes = 1000000
        partes = math.ceil(simples_lenght / tamanho_das_partes)
        nrows = tamanho_das_partes
        skiprows = 0

        print('Este arquivo será dividido em ' + str(partes) + ' partes para inserção no banco de dados')

        for i in range(0, partes):
            print('Iniciando a parte ' + str(i+1) + ' [...]')
            simples = pd.DataFrame(columns=[1,2,3,4,5,6])

            simples = pd.read_csv(filepath_or_buffer=extracted_file_path,
                                  sep=';',
                                  nrows=nrows,
                                  skiprows=skiprows,
                                  header=None,
                                  dtype=simples_dtypes,
                                  encoding='latin-1',
            )

            simples = simples.reset_index()
            del simples['index']

            simples.columns = ['cnpj_basico',
                           'opcao_pelo_simples_nacional',
                           'data_opcao_simples_nacional',
                           'data_exclusao_simples_nacional',
                           'opcao_pelo_mei',
                           'data_opcao_mei',
                           'data_exclusao_mei']

            #Tabela: tributacao
            #Colunas: cnpj_basico, opcao_pelo_simples_nacional, opcao_pelo_mei, data_opcao_simples_nacional, 
            # data_exclusao_simples_nacional, data_opcao_mei, data_exclusao_mei

            skiprows = skiprows+nrows

            to_sql(simples, name='tributacao', con=engine, if_exists='append', index=False)
            print('Arquivo ' + arquivos_simples[e] + ' inserido com sucesso no banco de dados! - Parte '+ str(i+1))

            try:
                del simples
            except:
                pass

    try:
        del simples
    except:
        pass

    print('Arquivos do simples finalizados!')
    simples_insert_end = time.time()
    simples_Tempo_insert = round((simples_insert_end - simples_insert_start))
    print('Tempo de execução do processo do Simples Nacional (em segundos): ' + str(simples_Tempo_insert))
