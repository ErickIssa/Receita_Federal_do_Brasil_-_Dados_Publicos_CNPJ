import requests
import re
from xml.etree import ElementTree as ET

def listar_diretorios(base_url):
    headers = {"Depth": "1"}
    resp = requests.request("PROPFIND", base_url, headers=headers)

    tree = ET.fromstring(resp.content)
    ns = {'d': 'DAV:'}

    dirs = []
    for response in tree.findall('d:response', ns):
        href = response.find('d:href', ns).text
        nome = href.rstrip('/').split('/')[-1]

        if re.match(r'\d{4}-\d{2}', nome):
            dirs.append(nome)

    return sorted(dirs, reverse=True)


def listar_arquivos_zip(base_url, dir_name):
    headers = {"Depth": "1"}
    url = base_url + f"{dir_name}/"

    resp = requests.request("PROPFIND", url, headers=headers)

    tree = ET.fromstring(resp.content)
    ns = {'d': 'DAV:'}

    files = []
    for response in tree.findall('d:response', ns):
        href = response.find('d:href', ns).text

        if href.lower().endswith('.zip'):
            files.append("https://arquivos.receitafederal.gov.br" + href)

    return files