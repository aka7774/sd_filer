import os
import pathlib
import yaml
import torch

from modules import sd_models
from modules.shared import opts, cmd_opts, state

from . import models as filer_models

def load_active_dir():
    return ''

def list(dirs):
    data = filer_models.load_comment('images')
    
    p = pathlib.Path(__file__).parts[-3]

    rs = []
    for filepath in dirs:
        if not os.path.exists(filepath):
            continue

        filename = os.path.basename(filepath)

        r = {}

        d = data[filename] if filename in data else {}

        r['title'] = filename
        r['filename'] = filename
        r['filepath'] = filepath
        r['files'] = sum(os.path.isfile(os.path.join(filepath, name)) for name in os.listdir(filepath))
        r['comment'] = d['comment'] if 'comment' in d else ''

        rs.append(r)

    return rs

def list_active():
    image_dirs = [
        opts.outdir_txt2img_samples,
        opts.outdir_img2img_samples,
        opts.outdir_extras_samples,
        opts.outdir_txt2img_grids,
        opts.outdir_img2img_grids,
        opts.outdir_save,
        os.path.join('extensions', 'generate_from_json', 'json'),
        os.path.join('extensions', 'generate_from_json', 'webp'),
    ]
    
    paths = os.path.join('extensions', 'stable-diffusion-webui-images-browser', 'path_recorder.txt')
    if os.path.exists(paths):
        with open(paths) as f:
            for line in f:
                image_dirs.append(line.rstrip("\r\n"))
    return list(image_dirs)

def list_backup():
    backup_dir = filer_models.load_backup_dir('images')
    if not backup_dir or not os.path.exists(backup_dir):
        return []

    dirs = []
    for dir in os.listdir(backup_dir):
        dirs.append(os.path.join(backup_dir, dir))
    return list(dirs)
