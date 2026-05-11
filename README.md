# Dados Públicos CNPJ
- Fonte oficial da Receita Federal do Brasil, [aqui](https://dados.gov.br/dados/conjuntos-dados/cadastro-nacional-da-pessoa-juridica---cnpj).
- Layout dos arquivos, [aqui](https://www.gov.br/receitafederal/dados/cnpj-metadados.pdf).

A Receita Federal do Brasil disponibiliza bases com os dados públicos do cadastro nacional de pessoas jurídicas (CNPJ).

De forma geral, nelas constam as mesmas informações que conseguimos ver no cartão do CNPJ, quando fazemos uma consulta individual, acrescidas de outros dados de Simples Nacional, sócios e etc. Análises muito ricas podem sair desses dados, desde econômicas, mercadológicas até investigações.

Nesse repositório consta um processo de ETL para **i)** baixar os arquivos; **ii)** descompactar; **iii)** ler, tratar e **iv)** inserir num banco de dados relacional SQLite.

---------------------

# Extração em Inglês e em Inglês

Para selecionar o idioma das tabelas que serão extraídas, deve-se trocar de branch no repositório antes de iniciar o processo de processamento ou build. Esta arquitetura garante que os esquemas de dados, cabeçalhos e metadados específicos de cada região permaneçam isolados, evitando a contaminação de traduções e garantindo a integridade dos dados locais.

- [Inglês](https://github.com/ErickIssa/Receita_Federal_do_Brasil_-_Dados_Publicos_CNPJ/tree/Ingles)
- [Português](https://github.com/ErickIssa/Receita_Federal_do_Brasil_-_Dados_Publicos_CNPJ/tree/Portugues)

### Infraestrutura necessária:
- [Python 3.8](https://www.python.org/downloads/release/python-3810/)
- [SQLite]

---------------------

### How to use:
1. Instale as bibliotecas necessárias, disponíveis em `requirements.txt`:
```bash
pip install -r requirements.txt
```

2. Execute o arquivo `src/main.py` a partir da raiz do projeto e siga as instruções para iniciar o processo de extração, carga ou processamento completo:
```bash
python src/main.py
```
   - O projeto utiliza SQLite. O banco de dados (`cnpj_dados.db`) e as tabelas são criados automaticamente pela aplicação.
   - Os arquivos são grandes. Dependendo da infraestrutura isso deve levar muitas horas para conclusão.

---------------------

### Tabelas geradas:
- Para maiores informações, consulte o [layout](https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/cadastros/consultas/arquivos/NOVOLAYOUTDOSDADOSABERTOSDOCNPJ.pdf).
  - `empresa`: dados cadastrais da empresa em nível de matriz
  - `estabelecimento`: dados analíticos da empresa por unidade / estabelecimento (telefones, endereço, filial, etc)
  - `socio`: dados cadastrais dos sócios das empresas
  - `taxacao`: dados de MEI e Simples Nacional
  - `cnae`: código e descrição dos CNAEs
  - `qualificacao`: tabela de qualificação das pessoas físicas - sócios, responsável e representante legal.
  - `natureza_juridica`: tabela de naturezas jurídicas - código e descrição.
  - `motivo_situacao_cadastral`: tabela de motivos da situação cadastral - código e descrição.
  - `pais`: tabela de países - código e descrição.
  - `cidade`: tabela de municípios - código e descrição.
  - `porte_empresa`: tabela de porte da empresa.
  - `situacao_cadstral`: tabela de situação cadastral.
  - `tipo_socio`: tabela de identificador de sócio.
  - `faixa_etaria`: tabela de faixas etárias.


- Pelo volume de dados, as tabelas  `empresa`, `estabelecimento`, `socio` e `taxacao` possuem índices para a coluna `cnpj_basico`, que é a principal chave de ligação entre elas.

### Modelo de Entidade Relacionamento:
![alt text](https://github.com/ErickIssa/Receita_Federal_do_Brasil_-_Dados_Publicos_CNPJ/blob/Portugues/DiagramaBancoPT.png)
