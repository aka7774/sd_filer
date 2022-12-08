import os
import pathlib
import yaml
import torch

from modules import sd_models
from modules.shared import opts, cmd_opts, state
from modules.hypernetworks import hypernetwork
from . import models as filer_models

def load_active_dir():
    return cmd_opts.hypernetwork_dir

def state(tab2, filename):
    if tab2 == 'active':
        filepath = os.path.join(cmd_opts.hypernetwork_dir, filename)
    else:
        backup_dir = filer_models.load_backup_dir()
        if not backup_dir or not os.path.exists(backup_dir):
            return {}
        filepath = os.path.join(backup_dir, filename)

    r = {}
    state_dict = torch.load(filepath, map_location='cpu')
    r['name'] = state_dict.get('name', None)
    r['layer_structure'] = state_dict.get('layer_structure', [1, 2, 1])
    r['activation_func'] = state_dict.get('activation_func', None)
    r['weight_init'] = state_dict.get('weight_initialization', 'Normal')
    r['add_layer_norm'] = state_dict.get('is_layer_norm', False)
    r['use_dropout'] = state_dict.get('use_dropout', False)
    r['activate_output'] = state_dict.get('activate_output', True)
    r['last_layer_dropout'] = state_dict.get('last_layer_dropout', False)
    optimizer_saved_dict = torch.load(filepath + '.optim', map_location = 'cpu') if os.path.exists(filepath + '.optim') else {}
    r['optimizer_name'] = optimizer_saved_dict.get('optimizer_name', 'AdamW')
    r['optimizer_hash'] = optimizer_saved_dict.get('hash', None)
    r['optimizer_state_dict'] = optimizer_saved_dict.get('optimizer_state_dict', None)

    return r

def list(dir):
    data = filer_models.load_comment('hypernetworks')
    
    rs = []
    for filepath in hypernetwork.list_hypernetworks(dir).values():
        r = {}

        filename = os.path.basename(filepath)
        d = data[filename] if filename in data else {}

        r['title'] = filename
        r['filename'] = filename
        r['filepath'] = filepath
        r['hash'] = sd_models.model_hash(r['filepath'])
        r['sha256_path'] = r['filepath'] + '.sha256'
        r['sha256'] = pathlib.Path(r['sha256_path']).read_text()[:8]+'...' if os.path.exists(r['sha256_path']) else ''
        r['model'] = d['model'] if 'model' in d else ''
        r['comment'] = d['comment'] if 'comment' in d else ''

        rs.append(r)

    return rs

def list_active():
    return list(cmd_opts.hypernetwork_dir)

def list_backup():
    backup_dir = filer_models.load_backup_dir()
    if not backup_dir or not os.path.exists(backup_dir):
        return []

    return list(backup_dir)
