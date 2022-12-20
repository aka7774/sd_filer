import os
import pathlib

from modules import sd_models
from . import models as filer_models

files = [
    'config.json',
    'ui-config.json',
    os.path.join('extensions', 'stable-diffusion-webui-images-browser', 'path_recorder.txt'),
    os.path.join('extensions', 'sdweb-merge-block-weighted-gui', 'csv', 'history.tsv'),
    os.path.join('extensions', 'sdweb-merge-block-weighted-gui', 'csv', 'preset.tsv'),
    ]

def get_list():
    rs = []
    for filepath in files:
        if not os.path.exists(filepath):
            continue

        filename = os.path.basename(filepath)
        r = {}
        r['title'] = filename
        r['filename'] = filename
        r['filepath'] = os.path.abspath(filepath)

        rs.append(r)

    return rs

def load(filename):
    for filepath in files:
        if filename != os.path.basename(filepath):
            continue
        if not os.path.exists(filepath):
            continue
        with open(filepath, 'r') as f:
            text = f.read()
        return text.encode().decode('unicode-escape')
    raise ValueError(f"{filename} not found.")

def download(filename):
    for filepath in files:
        if filename != os.path.basename(filepath):
            continue
        if not os.path.exists(filepath):
            continue
        return filepath
    raise ValueError(f"{filename} not found.")

def save(filename, text):
    for filepath in files:
        if filename != os.path.basename(filepath):
            continue
        if not os.path.exists(filepath):
            continue
        with open(filepath, 'w') as f:
            f.write(text)
        return f"{filename} saved."
    raise ValueError(f"{filename} not found.")

def table():
    name = 'files'
    rs = get_list()

    code = f"""
    <table>
        <thead>
            <tr>
                <th>Filename</th>
                <th>Filepath</th>
                <th>Edit</th>
                <th>Download</th>
            </tr>
        </thead>
        <tbody>
    """

    for r in rs:
        code += f"""
            <tr class="filer_{name}_row" data-title="{r['title']}">
                <td class="filer_filename">{r['filename']}</td>
                <td class="filer_filepath">{r['filepath']}</td>
                <td class="filer_load"><input onclick="load_{name}(this, '{r['title']}')" type="button" value="Load" class="gr-button gr-button-lg gr-button-secondary"></td>
                <td class="filer_download"><input onclick="download_{name}(this, '{r['title']}')" type="button" value="Download" class="gr-button gr-button-lg gr-button-secondary"></td>
            </tr>
            """

    code += """
        </tbody>
    </table>
    """

    return code