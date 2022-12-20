import os
import pathlib

from modules import sd_models
from . import models as filer_models
from . import actions as filer_actions

def load_active_dir():
    return "models/lora"

def get_list(dir):
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
    return get_list(load_active_dir())

def list_backup():
    backup_dir = filer_models.load_backup_dir('loras')
    if not backup_dir or not os.path.exists(backup_dir):
        return []
    return get_list(backup_dir)
    
def urls(urls):
    return filer_actions.urls(urls, load_active_dir())

def table(name, rs):
    code = f"""
    <table>
        <thead>
            <tr>
                <th></th>
                <th>Filename</th>
                <th>sha256</th>
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
                <td class="filer_sha256">{r['sha256']}</td>
                <td><input class="filer_comment" type="text" value="{r['comment']}"></td>
            </tr>
            """

    code += """
        </tbody>
    </table>
    """

    return code
