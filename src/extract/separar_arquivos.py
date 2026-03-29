import os

def separar_arquivos(pasta):
    items = os.listdir(pasta)

    grupos = {
        "empresa": [],
        "estabelecimento": [],
        "socios": [],
        "simples": [],
        "cnae": [],
        "moti": [],
        "munic": [],
        "natju": [],
        "pais": [],
        "quals": []
    }

    for item in items:
        for chave in grupos:
            if chave.upper() in item:
                grupos[chave].append(item)

    return grupos