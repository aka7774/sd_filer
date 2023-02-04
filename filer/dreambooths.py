import os
import pathlib

from modules import sd_models, shared
from .base import FilerGroupBase
from . import models as filer_models

class FilerGroupDreambooths(FilerGroupBase):
    name = 'dreambooths'
    upload_zip = True

    @classmethod
    def get_active_dir(cls):
        models_path = None
        try:
            models_path = shared.cmd_opts.dreambooth_models_path
        except:
            pass
        if models_path == "" or models_path is None:
            models_path = os.path.join(shared.models_path, "dreambooth")

        return os.path.abspath(models_path)

    @classmethod
    def _get_list(cls, dir):
        rs = []
        for filename in os.listdir(dir):
            # ファイルは対象外
            if not os.path.isdir(os.path.join(dir, filename)):
                continue

            r = {}
            r['title'] = filename
            r['filename'] = filename
            r['filepath'] = os.path.join(dir, filename)

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
                    <th>name</th>
                </tr>
            </thead>
            <tbody>
        """

        for r in rs:
            code += f"""
                <tr class="filer_{name}_row" data-title="{r['title']}">
                    <td class="filer_checkbox"><input class="filer_{name}_select" type="checkbox" onClick="rows_{name}()"></td>
                    <td class="filer_filename">{r['filename']}</td>
                </tr>
                """

        code += """
            </tbody>
        </table>
        """

        return code
