import os
import pathlib
import yaml
import torch

from modules import sd_models
from modules.shared import opts, cmd_opts, state

from .base import FilerGroupBase
from . import models as filer_models

class FilerGroupImages(FilerGroupBase):
    name = 'images'
    upload_zip = True

    @classmethod
    def get_active_dir(cls):
        return os.path.abspath(".")

    @classmethod
    def _get_list(cls, dirs, parent_dir = ''):
        data = filer_models.load_comment(cls.name)
        
        for dir in dirs:
            for filedir, subdirs, filenames in os.walk(dir):
                for subdir in subdirs:
                    sub_path = os.path.join(filedir, subdir)
                    if os.path.isdir(sub_path):
                        dirs.append(sub_path)

        rs = []
        for filepath in dirs:
            if not os.path.exists(filepath):
                continue

            filename = os.path.basename(filepath)

            r = {}

            d = data[filename] if filename in data else {}

            r['filename'] = filename
            r['filepath'] = filepath
            r['title'] = cls.get_rel_path(parent_dir, os.path.abspath(r['filepath']))
            r['files'] = sum(os.path.isfile(os.path.join(r['filepath'], name)) for name in os.listdir(r['filepath']))
            r['comment'] = d['comment'] if 'comment' in d else ''

            rs.append(r)

        return rs

    @classmethod
    def list_active(cls):
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
        return cls._get_list(image_dirs, cls.get_active_dir())

    @classmethod
    def list_backup(cls):
        backup_dir = filer_models.load_backup_dir(cls.name)
        if not backup_dir or not os.path.exists(backup_dir):
            return []
        dirs = []
        for dir in os.listdir(backup_dir):
            dirs.append(os.path.join(backup_dir, dir))
        return cls._get_list(dirs, backup_dir)

    @classmethod
    def list_append(cls, filename):
        paths = os.path.join('extensions', 'stable-diffusion-webui-images-browser', 'path_recorder.txt')
        if os.path.exists(paths):
            with open(paths, 'a+') as f:
                f.seek(0)
                # 既に存在すれば何もしない
                for line in f:
                    dir = line.rstrip("\r\n")
                    if (dir == filename):
                        return
                # 存在しなければ末尾に追加
                f.seek(0, 2)
                f.write(f"{filename}\n")

    @classmethod
    def _table(cls, name, rs):
        name = f"{cls.name}_{name}"
        code = f"""
        <table>
            <thead>
                <tr>
                    <th></th>
                    <th>Filepath</th>
                    <th>files</th>
                    <th>Comment</th>
                </tr>
            </thead>
            <tbody>
        """

        for r in rs:
            code += f"""
                <tr class="filer_{name}_row" data-title="{r['title']}">
                    <td class="filer_checkbox"><input class="filer_{name}_select" type="checkbox" onClick="rows_{name}()"></td>
                    <td class="filer_title">{r['title']}</td>
                    <td class="filer_files">{r['files']}</td>
                    <td>{r['comment']}</td>
                </tr>
                """

        code += """
            </tbody>
        </table>
        """

        return code
