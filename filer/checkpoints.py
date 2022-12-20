import os
import pathlib
import yaml
import torch
from safetensors.torch import save_file

from modules import sd_models
from . import models as filer_models

def load_active_dir():
    for c in sd_models.checkpoints_list.values():
        return os.path.dirname(c.filename)

def get_list(dir):
    data = filer_models.load_comment('checkpoints')
    rs = []
    for filename in os.listdir(dir):
        if not filename.endswith('.ckpt') and not filename.endswith('.safetensors') and not filename.endswith('.vae.pt'):
            continue

        d = data[filename] if filename in data else {}

        r = {}
        r['title'] = filename
        r['filename'] = filename
        r['filepath'] = os.path.join(dir, filename)
        r['hash'] = sd_models.model_hash(r['filepath'])
        r['sha256_path'] = r['filepath'] + '.sha256'
        r['sha256'] = pathlib.Path(r['sha256_path']).read_text()[:16] if os.path.exists(r['sha256_path']) else ''
        r['vae_path'] = os.path.splitext(r['filepath'])[0] + '.vae.pt'
        r['vae'] = 'Y' if os.path.exists(r['vae_path']) else ''
        r['yaml_path'] = os.path.splitext(r['filepath'])[0] + '.yaml'
        r['yaml'] = 'Y' if os.path.exists(r['yaml_path']) else ''
        r['genre'] = d['genre'] if 'genre' in d else ''
        r['comment'] = d['comment'] if 'comment' in d else ''

        rs.append(r)

    return rs

def list_active():
    return get_list(load_active_dir())

def list_backup():
    backup_dir = filer_models.load_backup_dir('checkpoints')
    if not backup_dir or not os.path.exists(backup_dir):
        return []
    return get_list(backup_dir)

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

def convert_safetensors(filenames, list):
    for r in list:
        if r['filename'] not in filenames.split(','):
            continue
        if not r['filename'].endswith('.ckpt'):
            continue

        dst_path = os.path.splitext(r['filepath'])[0] + '.safetensors'

        with torch.no_grad():
            weights = torch.load(r['filepath'])["state_dict"]
            save_file(weights, dst_path)
            print(f"{dst_path} saved.")
    return "converted."

def table(name, rs):
    code = f"""
    <table>
        <thead>
            <tr>
                <th></th>
                <th>Filename</th>
                <th>hash</th>
                <th>sha256</th>
                <th>vae.pt</th>
                <th>yaml</th>
                <th>Genre</th>
                <th>Comment</th>
            </tr>
        </thead>
        <tbody>
    """

    for r in rs:
        op_html = ''
        for op in ['Default', 'Merged', 'Dreambooth', 'DreamArtist']:
            if op == r['genre']:
                op_html += '<option selected>' + op
            else:
                op_html += '<option>' + op

        code += f"""
            <tr class="filer_{name}_row" data-title="{r['title']}">
                <td class="filer_checkbox"><input class="filer_{name}_select" type="checkbox" onClick="rows_{name}()"></td>
                <td class="filer_filename">{r['filename']}</td>
                <td class="filer_hash">{r['hash']}</td>
                <td class="filer_sha256">{r['sha256']}</td>
                <td class="filer_vae">{r['vae']}</td>
                <td class="filer_yaml">{r['yaml']}</td>
                <td><select class="filer_genre">{op_html}</select></td>
                <td><input class="filer_comment" type="text" value="{r['comment']}"></td>
            </tr>
            """

    code += """
        </tbody>
    </table>
    """

    return code
