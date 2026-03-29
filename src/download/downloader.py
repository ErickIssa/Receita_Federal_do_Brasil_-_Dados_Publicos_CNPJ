import os
import requests
from src.utils.file_utils import check_diff

def baixar_arquivo(url, pasta):
    local = os.path.join(pasta, url.split('/')[-1])

    if not check_diff(url, local):
        print(f"[Pulado] {local}")
        return

    print(f"[Baixando] {url}")

    resp = requests.get(url, stream=True)

    with open(local, 'wb') as f:
        for chunk in resp.iter_content(8192):
            if chunk:
                f.write(chunk)

    print(f"[OK] {local}")