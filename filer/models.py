import os
import pathlib
import json

from modules import script_callbacks, sd_models, shared

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

def load_genre_comment():
    p = pathlib.Path(__file__).parts[-4:-2]
    filepath = os.path.join(p[0], p[1], 'json', 'checkpoints.json')
    if os.path.exists(filepath):
        with open(filepath) as f:
            return json.load(f)
    return {}

def list_checkpoints_active():
    data = load_genre_comment()
    rs = []
    for c in sd_models.checkpoints_list.values():
        filename = os.path.basename(c.filename)
        d = data[filename] if filename in data else {}

        r = {}
        r['title'] = filename
        r['filename'] = filename
        r['filepath'] = c.filename
        r['hash'] = c.hash
        r['sha256_path'] = r['filepath'] + '.sha256'
        r['sha256'] = pathlib.Path(r['sha256_path']).read_text()[:8]+'...' if os.path.exists(r['sha256_path']) else ''
        r['vae_path'] = os.path.splitext(r['filepath'])[0] + '.vae.pt'
        r['vae'] = 'Y' if os.path.exists(r['vae_path']) else ''
        r['yaml_path'] = os.path.splitext(r['filepath'])[0] + '.yaml'
        r['yaml'] = 'Y' if os.path.exists(r['yaml_path']) else ''
        r['genre'] = d['genre'] if 'genre' in d else ''
        r['comment'] = d['comment'] if 'comment' in d else ''

        rs.append(r)

    return rs

def list_checkpoints_backup():
    backup_dir = load_backup_dir()
    if not backup_dir or not os.path.exists(backup_dir):
        return []

    data = load_genre_comment()
    rs = []
    for filename in os.listdir(backup_dir):
        if not filename.endswith('.ckpt') and not filename.endswith('.safetensor'):
            continue

        d = data[filename] if filename in data else {}

        r = {}
        r['title'] = filename
        r['filename'] = filename
        r['filepath'] = os.path.join(backup_dir, filename)
        r['hash'] = sd_models.model_hash(r['filepath'])
        r['sha256_path'] = r['filepath'] + '.sha256'
        r['sha256'] = pathlib.Path(r['sha256_path']).read_text()[:8]+'...' if os.path.exists(r['sha256_path']) else ''
        r['vae_path'] = os.path.splitext(r['filepath'])[0] + '.vae.pt'
        r['vae'] = 'Y' if os.path.exists(r['vae_path']) else ''
        r['yaml_path'] = os.path.splitext(r['filepath'])[0] + '.yaml'
        r['yaml'] = 'Y' if os.path.exists(r['yaml_path']) else ''
        r['genre'] = d['genre'] if 'genre' in d else ''
        r['comment'] = d['comment'] if 'comment' in d else ''

        rs.append(r)

    return rs
