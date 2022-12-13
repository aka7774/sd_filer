import os
import pathlib

from modules import sd_models
from . import models as filer_models

def load_active_dir():
    return "models/dreambooth"

def list(dir):
    data = filer_models.load_comment('dreambooths')
    rs = []
    for filename in os.listdir(dir):
        # ファイルは対象外
        if not os.path.isdir(os.path.join(dir, filename)):
            continue

        d = data[filename] if filename in data else {}

        r = {}
        r['title'] = filename
        r['filename'] = filename
        r['filepath'] = os.path.join(dir, filename)
        r['comment'] = d['comment'] if 'comment' in d else ''

        rs.append(r)

    return rs

def list_active():
    return list(load_active_dir())

def list_backup():
    backup_dir = filer_models.load_backup_dir('dreambooths')
    if not backup_dir or not os.path.exists(backup_dir):
        return []
    return list(backup_dir)
