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
        for filedir, subdirs, filenames in os.walk(dir):
            for filename in filenames:
                if not filename.endswith('.pt'):
                    continue

                d = data[filename] if filename in data else {}

                r = {}
                r['filename'] = filename
                r['filepath'] = os.path.join(filedir, filename)
                r['title'] = cls.get_rel_path(dir, r['filepath'])
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
                    <td class="filer_sha256">{r['sha256']}</td>
                    <td>{r['comment']}</td>
                </tr>
                """

        code += """
            </tbody>
        </table>
        """

        return code
