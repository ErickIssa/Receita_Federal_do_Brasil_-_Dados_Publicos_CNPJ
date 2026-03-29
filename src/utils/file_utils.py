import os
import requests

def check_diff(url, file_name):
    if not os.path.isfile(file_name):
        return True

    response = requests.head(url)
    new_size = int(response.headers.get('content-length', 0))
    old_size = os.path.getsize(file_name)

    if new_size != old_size:
        os.remove(file_name)
        return True

    return False


def makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)