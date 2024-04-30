import json

_settings_obj = {}


def get_settings():
    return _settings_obj


def _init_module():
    global _settings_obj

    with open('./settings.json', 'r') as f:
        file_content = f.read()
        _settings_obj = json.loads(file_content)


_init_module()
