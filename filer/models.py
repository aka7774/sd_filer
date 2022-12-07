import os
import pathlib
import json

from modules import sd_models

def get_dst_dir(src):
    if src == 'active':
        return load_backup_dir()
    else:
        return load_active_dir()

def load_active_dir():
    for c in sd_models.checkpoints_list.values():
        return os.path.dirname(c.filename)

def load_backup_dir():
    p = pathlib.Path(__file__).parts[-4:-2]
    filepath = os.path.join(p[0], p[1], 'json', 'config.json')
    data = {}
    if os.path.exists(filepath):
        with open(filepath) as f:
            data = json.load(f)
            return data['backup_dir']
    return ''

def save_backup_dir(backup_dir):
    p = pathlib.Path(__file__).parts[-4:-2]
    filepath = os.path.join(p[0], p[1], 'json', 'config.json')
    data = {}
    if os.path.exists(filepath):
        with open(filepath) as f:
            data = json.load(f)
    data.update({'backup_dir': backup_dir})
    with open(filepath, "w") as f:
        json.dump(data, f)

def load_comment(name):
    p = pathlib.Path(__file__).parts[-4:-2]
    filepath = os.path.join(p[0], p[1], 'json', f"{name}.json")
    if os.path.exists(filepath):
        with open(filepath) as f:
            return json.load(f)
    return {}

def save_comment(name, input):
    p = pathlib.Path(__file__).parts[-4:-2]
    filepath = os.path.join(p[0], p[1], 'json', f"{name}.json")
    data = {}
    if os.path.exists(filepath):
        with open(filepath) as f:
            data = json.load(f)
    data.update(json.loads(input))
    with open(filepath, "w") as f:
        json.dump(data, f)
    print("Done!")
