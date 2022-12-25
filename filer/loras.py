import os
import pathlib

from modules import sd_models
from .base import FilerGroupBase
from . import models as filer_models
from . import actions as filer_actions

class FilerGroupLoras(FilerGroupBase):
    name = 'loras'

    @classmethod
    def get_active_dir(cls):
        return os.path.abspath("models/lora")

    @classmethod
    def _get_list(cls, dir):
        data = filer_models.load_comment(cls.name)
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

    @classmethod
    def _table(cls, name, rs):
        name = f"{cls.name}_{name}"
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
