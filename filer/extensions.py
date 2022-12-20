import os
import pathlib
import yaml
import torch

from modules import sd_models
from modules.shared import opts, cmd_opts, state
from modules.extensions import extensions_dir

from . import models as filer_models

def load_active_dir():
    return extensions_dir

def get_list(dir):
    data = filer_models.load_comment('extensions')
    
    p = pathlib.Path(__file__).parts[-3]

    rs = []
    for filename in os.listdir(dir):
        # 自分自身は対象外
        if filename == p:
            continue
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
    return get_list(load_active_dir())

def list_backup():
    backup_dir = filer_models.load_backup_dir('extensions')
    if not backup_dir or not os.path.exists(backup_dir):
        return []

    return get_list(backup_dir)

def table(name, rs):
    code = f"""
    <table>
        <thead>
            <tr>
                <th></th>
                <th>name</th>
                <th>Comment</th>
            </tr>
        </thead>
        <tbody>
    """

    for r in rs:
        code += f"""
            <tr class="filer_{name}_row" data-title="{r['title']}">
                <td class="filer_checkbox"><input class="filer_{name}_select" type="checkbox" onClick="rows_{name}()"></td>
                <td class="filer_filename">{r['filename']}</td>
                <td><input class="filer_comment" type="text" value="{r['comment']}"></td>
            </tr>
            """

    code += """
        </tbody>
    </table>
    """

    return code
