import os
import pathlib
import yaml
import torch
from safetensors.torch import save_file

from modules import sd_models, shared
from .base import FilerGroupBase
from . import models as filer_models
from . import actions as filer_actions

class FilerGroupCheckpoints(FilerGroupBase):
    name = 'checkpoints'

    @classmethod
    def get_active_dir(cls):
        return shared.cmd_opts.ckpt_dir or sd_models.model_path

    @classmethod
    def _get_list(cls, dir):
        rs = []
        for filedir, subdirs, filenames in os.walk(dir):
            for filename in filenames:
                if not filename.endswith('.ckpt') and not filename.endswith('.safetensors') and not filename.endswith('.vae.pt'):
                    continue

                r = {}
                r['filename'] = filename
                r['filepath'] = os.path.join(filedir, filename)
                r['title'] = cls.get_rel_path(dir, r['filepath'])
                r['hash'] = sd_models.model_hash(r['filepath'])
                r['sha256_path'] = r['filepath'] + '.sha256'
                r['sha256'] = pathlib.Path(r['sha256_path']).read_text()[:10] if os.path.exists(r['sha256_path']) else ''
                r['vae_path'] = os.path.splitext(r['filepath'])[0] + '.vae.pt'
                r['vae'] = 'Y' if os.path.exists(r['vae_path']) else ''
                r['yaml_path'] = os.path.splitext(r['filepath'])[0] + '.yaml'
                r['yaml'] = 'Y' if os.path.exists(r['yaml_path']) else ''

                rs.append(r)

        return rs

    @classmethod
    def make_yaml(cls, filenames, list):
        y = {}
        for r in list:
            if r['title'] not in filenames.split(','):
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
    
    @classmethod
    def make_active(cls, filenames):
        html = '<pre>' + cls.make_yaml(filenames, cls.list_active()) + '</pre>'
        return html

    @classmethod
    def make_backup(cls, filenames):
        html = '<pre>' + cls.make_yaml(filenames, cls.list_backup()) + '</pre>'
        return html

    @classmethod
    def _table(cls, tab2, rs):
        name = f"{cls.name}_{tab2}"

        code = f"""
        <table>
            <thead>
                <tr>
                    <th></th>
                    <th>Filepath</th>
                    <th>shorthash</th>
                    <th>OLD hash</th>
                    <th>vae.pt</th>
                    <th>yaml</th>
                </tr>
            </thead>
            <tbody>
        """

        for r in rs:
            code += f"""
                <tr class="filer_{name}_row" data-title="{r['title']}">
                    <td class="filer_checkbox"><input class="filer_{name}_select" type="checkbox" onClick="rows_{name}()"></td>
                    <td class="filer_title">{r['title']}</td>
                    <td class="filer_sha256">{r['sha256']}</td>
                    <td class="filer_hash">{r['hash']}</td>
                    <td class="filer_vae">{r['vae']}</td>
                    <td class="filer_yaml">{r['yaml']}</td>
                </tr>
                """

        code += """
            </tbody>
        </table>
        """

        return code
