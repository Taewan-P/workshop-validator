import os, json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_SECRET_DIR = os.path.join(BASE_DIR, '.config_secret')
secret_file = os.path.join(CONFIG_SECRET_DIR, 'server_info.json')

def get_server_info_value(key: str):
    with open(secret_file, mode='rt', encoding='utf-8') as file:
        data = json.load(file)
        for k, v in data.items():
            if k == key:
                return v
        raise ValueError('Cannot find server information.')