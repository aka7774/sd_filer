import os
import pathlib
import yaml
import torch
from safetensors.torch import save_file

from modules import sd_models
from . import models as filer_models
from . import actions as filer_actions

class FilerGroupBase:
    name = ''
    upload_zip = False

    @classmethod
    def get_active_dir(cls):
        return ''

    @classmethod
    def _get_list(cls, dir):
        pass

    @classmethod
    def list_active(cls):
        return cls._get_list(cls.get_active_dir())

    @classmethod
    def list_backup(cls):
        backup_dir = filer_models.load_backup_dir(cls.name)
        if not backup_dir or not os.path.exists(backup_dir):
            return []
        return cls._get_list(backup_dir)

    @classmethod
    def download_urls(cls, urls):
        filer_actions.urls(urls, cls.get_active_dir())
        return 'Downloaded.'

    @classmethod
    def copy_active(cls, filenames):
        filer_actions.copy(filenames, cls.list_active(), filer_models.load_backup_dir(cls.name))
        return cls.table_active()

    @classmethod
    def copy_backup(cls, filenames):
        filer_actions.copy(filenames, cls.list_backup(), cls.get_active_dir())
        return cls.table_backup()

    @classmethod
    def move_active(cls, filenames):
        filer_actions.move(filenames, cls.list_active(), filer_models.load_backup_dir(cls.name))
        return cls.table_active()

    @classmethod
    def move_backup(cls, filenames):
        filer_actions.move(filenames, cls.list_backup(), cls.get_active_dir())
        return cls.table_backup()

    @classmethod
    def delete_active(cls, filenames):
        filer_actions.delete(filenames, cls.list_active())
        return cls.table_active()

    @classmethod
    def delete_backup(cls, filenames):
        filer_actions.delete(filenames, cls.list_backup())
        return cls.table_backup()

    @classmethod
    def calc_active(cls, filenames):
        filer_actions.calc_sha256(filenames, cls.list_active())
        return cls.table_active()

    @classmethod
    def calc_backup(cls, filenames):
        filer_actions.calc_sha256(filenames, cls.list_backup())
        return cls.table_backup()

    @classmethod
    def save_comment(cls, data):
        filer_models.save_comment(cls.name, data)
        return 'saved.'

    @classmethod
    def download_active(cls, filenames):
        return filer_actions.download(filenames, cls.list_active())

    @classmethod
    def download_backup(cls, filenames):
        return filer_actions.download(filenames, cls.list_backup())

    @classmethod
    def upload_active(cls, files):
        return filer_actions.upload(files, cls.get_active_dir(), cls.upload_zip)

    @classmethod
    def upload_backup(cls, files):
        return filer_actions.upload(files, filer_models.load_backup_dir(cls.name), cls.upload_zip)

    @classmethod
    def table_active(cls):
        return cls._table("active", cls.list_active())

    @classmethod
    def table_backup(cls):
        return cls._table("backup", cls.list_backup())

    @classmethod
    def reload_active(cls):
        return [cls.table_active(), '']

    @classmethod
    def reload_backup(cls):
        return [cls.table_backup(), '']

    @classmethod
    def _table(cls, name, rs):
        pass
