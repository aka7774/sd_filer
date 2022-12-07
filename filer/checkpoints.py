import os
import pathlib
import yaml

from modules import sd_models
from . import models as filer_models

def list_active():
    data = filer_models.load_comment('checkpoints')
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

def list_backup():
    backup_dir = filer_models.load_backup_dir()
    if not backup_dir or not os.path.exists(backup_dir):
        return []

    data = filer_models.load_comment('checkpoints')
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

def make_yaml(filenames, list):
    y = {}
    for r in list:
        if r['filename'] not in filenames.split(','):
            continue

        y[r['filename']] = {
            'description': r['title'],
            'weights': r['filepath'],
            'config': 'configs/stable-diffusion/v1-inference.yaml',
            'width': 512,
            'height': 512,
        }
        # 1111のデフォルトのconfig値は使わない
        if os.path.exists(r['yaml_path']):
            y[r['filename']]['config'] = r['yaml_path']
        if os.path.exists(r['vae_path']):
            y[r['filename']]['vae'] = r['vae_path']

    return yaml.dump(y)
