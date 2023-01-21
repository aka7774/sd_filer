import os
import pathlib
import json

from modules import sd_models

default_settings = {
    'backup_dir': '',
    'backup_checkpoints_dir': '',
    'backup_embeddings_dir': '',
    'backup_dreambooths_dir': '',
    'backup_loras_dir': '',
    'backup_hypernetworks_dir': '',
    'backup_extensions_dir': '',
    'backup_images_dir': '',
    }
def load_settings():
    p = pathlib.Path(__file__).parts[-4:-2]
    filepath = os.path.join(p[0], p[1], 'config', 'config.json')
    settings = default_settings
    if os.path.exists(filepath):
        with open(filepath) as f:
            settings.update(json.load(f))
    return settings

def load_backup_dir(name):
    settings = load_settings()

    dir = ''
    if 'backup_'+name+'_dir' in settings and settings['backup_'+name+'_dir']:
        dir = settings['backup_'+name+'_dir']
    elif 'backup_dir' in settings and settings['backup_dir']:
        dir = os.path.join(settings['backup_dir'], name)

    if dir and not os.path.exists(dir):
        os.makedirs(dir)

    return dir

def save_settings(*input_settings):
    p = pathlib.Path(__file__).parts[-4:-2]
    filepath = os.path.join(p[0], p[1], 'config', 'config.json')
    data = {}
    if os.path.exists(filepath):
        with open(filepath) as f:
            data = json.load(f)
    i = 0
    for k in default_settings.keys():
        data.update({k: input_settings[i]})
        i += 1
    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))
    with open(filepath, "w") as f:
        json.dump(data, f)
    return json.dumps(data)
