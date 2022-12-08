import os
import pathlib
import json

from modules import sd_models

def load_settings():
    p = pathlib.Path(__file__).parts[-4:-2]
    filepath = os.path.join(p[0], p[1], 'json', 'config.json')
    settings = {
        'backup_dir': '',
        'backup_checkpoints_dir': '',
        'backup_hypernetworks_dir': '',
        'backup_extensions_dir': '',
        'backup_images_dir': '',
    }
    if os.path.exists(filepath):
        with open(filepath) as f:
            settings.update(json.load(f))
    return settings

def load_backup_dir(name):
    settings = load_settings()

    dir = ''
    if settings['backup_'+name+'_dir']:
        dir = settings['backup_'+name+'_dir']
    elif settings['backup_dir']:
        dir = os.path.join(settings['backup_dir'], name)

    if dir and not os.path.exists(dir):
        os.makedirs(dir)

    return dir

def save_settings(backup_dir,
                backup_checkpoints_dir,
                backup_hypernetworks_dir,
                backup_extensions_dir,
                backup_images_dir):
    p = pathlib.Path(__file__).parts[-4:-2]
    filepath = os.path.join(p[0], p[1], 'json', 'config.json')
    data = {}
    if os.path.exists(filepath):
        with open(filepath) as f:
            data = json.load(f)
    data.update({'backup_dir': backup_dir})
    data.update({'backup_checkpoints_dir': backup_checkpoints_dir})
    data.update({'backup_hypernetworks_dir': backup_hypernetworks_dir})
    data.update({'backup_extensions_dir': backup_extensions_dir})
    data.update({'backup_images_dir': backup_images_dir})
    with open(filepath, "w") as f:
        json.dump(data, f)
    return json.dumps(data)

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
