import pathlib
import os

BASE_URL = 'https://arquivos.receitafederal.gov.br/public.php/dav/files/gn672Ad4CF8N6TK/Dados/Cadastros/CNPJ/'

BASE_PATH = pathlib.Path().resolve()

OUTPUT_FILES = os.path.join(BASE_PATH, 'output_files')
EXTRACTED_FILES = os.path.join(BASE_PATH, 'extracted_files')

DATABASE = 'cnpj_dados_PT.db'