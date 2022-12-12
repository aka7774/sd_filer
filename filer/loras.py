import os
import pathlib
import yaml

from modules import sd_models
from . import models as filer_models

def load_active_dir():
    return "models/lora"

def list(dir):
    data = filer_models.load_comment('loras')
    rs = []
    for filename in os.listdir(dir):
        if not filename.endswith('.pt'):
            continue

        d = data[filename] if filename in data else {}

        r = {}
        r['title'] = filename
        r['filename'] = filename
        r['filepath'] = os.path.join(dir, filename)
        r['sha256_path'] = r['filepath'] + '.sha256'
        r['sha256'] = pathlib.Path(r['sha256_path']).read_text()[:16] if os.path.exists(r['sha256_path']) else ''
        r['comment'] = d['comment'] if 'comment' in d else ''

        rs.append(r)

    return rs

def list_active():
    return list(load_active_dir())

def list_backup():
    backup_dir = filer_models.load_backup_dir('loras')
    if not backup_dir or not os.path.exists(backup_dir):
        return []
    return list(backup_dir)
