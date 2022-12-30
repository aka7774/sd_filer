import os
import pathlib
import yaml
import torch
import pprint

from modules import sd_models
from modules.shared import opts, cmd_opts, state
from modules.hypernetworks import hypernetwork

from .base import FilerGroupBase
from . import models as filer_models
from . import actions as filer_actions

class FilerGroupHypernetworks(FilerGroupBase):
    name = 'hypernetworks'

    @classmethod
    def get_active_dir(cls):
        return cmd_opts.hypernetwork_dir

    @classmethod
    def state(cls, tab2, filename):
        
        filepath = os.path.join(cls.get_dir(tab2), filename)
        
        if not os.path.exists(filepath):
            raise ValueError(f"Not found {filepath}")

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

    @classmethod
    def state_active(cls, title):
        html = title + '<br><pre>' + pprint.pformat(cls.state('active', title)) + '</pre>'
        return html

    @classmethod
    def state_backup(cls, title):
        html = title + '<br><pre>' + pprint.pformat(cls.state('backup', title)) + '</pre>'
        return html

    @classmethod
    def _get_list(cls, dir):
        data = filer_models.load_comment(cls.name)
    
        rs = []
        for filedir, subdirs, filenames in os.walk(dir):
            for filename in filenames:
                if not filename.endswith('.pt'):
                    continue

                r = {}

                d = data[filename] if filename in data else {}

                r['filename'] = filename
                r['filepath'] = os.path.join(filedir, filename)
                r['title'] = cls.get_rel_path(dir, r['filepath'])
                r['hash'] = sd_models.model_hash(r['filepath'])
                r['sha256_path'] = r['filepath'] + '.sha256'
                r['sha256'] = pathlib.Path(r['sha256_path']).read_text()[:16] if os.path.exists(r['sha256_path']) else ''

                r['comment'] = d['comment'] if 'comment' in d else ''

                rs.append(r)

        return rs

    @classmethod
    def _table(cls, tab2, rs):
        name = f"{cls.name}_{tab2}"
        code = f"""
        <table>
            <thead>
                <tr>
                    <th></th>
                    <th>Filepath</th>
                    <th>state</th>
                    <th>hash</th>
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
                    <td class="filer_title">{r['title']}</td>
                    <td class="filer_state"><input onclick="state_{name}(this, '{r['title']}')" type="button" value="state" class="gr-button gr-button-lg gr-button-secondary"></td>
                    <td class="filer_hash">{r['hash']}</td>
                    <td class="filer_sha256">{r['sha256']}</td>
                    <td><input class="filer_comment" type="text" value="{r['comment']}"></td>
                </tr>
                """

        code += """
            </tbody>
        </table>
        """

        return code
