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

    for i in range(len(items)):
        if items[i].find('EMPRE') > -1:
            grupos['empresa'].append(items[i])
        elif items[i].find('ESTABELE') > -1:
            grupos['estabelecimento'].append(items[i])
        elif items[i].find('SOCIO') > -1:
            grupos['socios'].append(items[i])
        elif items[i].find('SIMPLES') > -1:
            grupos['simples'].append(items[i])
        elif items[i].find('CNAE') > -1:
            grupos['cnae'].append(items[i])
        elif items[i].find('MOTI') > -1:
            grupos['moti'].append(items[i])
        elif items[i].find('MUNIC') > -1:
            grupos['munic'].append(items[i])
        elif items[i].find('NATJU') > -1:
            grupos['natju'].append(items[i])
        elif items[i].find('PAIS') > -1:
            grupos['pais'].append(items[i])
        elif items[i].find('QUALS') > -1:
            grupos['quals'].append(items[i])
        else:
            pass

    return grupos