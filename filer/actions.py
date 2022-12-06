import os
import shutil
import pathlib
import json
import yaml
import hashlib

from modules.sd_models import checkpoints_list
from . import models as filer_models

def calc_hash(algo, filepath):
    # ハッシュオブジェクトを作ります
    h = hashlib.new(algo)

    # 分割する長さをブロックサイズの整数倍に決めます
    Length = hashlib.new(algo).block_size * 0x800

    # 大きなバイナリデータを用意します
    with open(filepath, 'rb') as f:
        BinaryData = f.read(Length)

        # データがなくなるまでループします
        while BinaryData:
            # ハッシュオブジェクトに追加して計算します。
            h.update(BinaryData)

            # データの続きを読み込む
            BinaryData = f.read(Length)

    # ハッシュオブジェクトを16進数で出力します
    return h.hexdigest()

def make_yaml(filenames, list):
    y = {}
    for r in list:
        if r['filename'] not in filenames.split(','):
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

def save_checkpoints(input):
    p = pathlib.Path(__file__).parts[-4:-2]
    filepath = os.path.join(p[0], p[1], 'json', 'checkpoints.json')
    data = {}
    if os.path.exists(filepath):
        with open(filepath) as f:
            data = json.load(f)
    data.update(json.loads(input))
    with open(filepath, "w") as f:
        json.dump(data, f)
    print("Done!")

def calc_sha256(filenames, list):
    for r in list:
        if r['filename'] not in filenames.split(','):
            continue

        r['sha256'] = calc_hash('sha256', r['filepath'])
        pathlib.Path(r['sha256_path']).write_text(r['sha256'], encoding="utf-8")
        print(f"{r['filepath']} sha256: {r['sha256']}")
    print("Done!")

def copy_checkpoints(filenames, list, src):
    dst_dir = filer_models.get_dst_dir(src)
    for r in list:
        if r['filename'] not in filenames.split(','):
            continue

        dst_path = os.path.join(dst_dir, r['filename'])
        
        if os.path.exists(dst_path):
            print(f"Already exists: {dst_path}")
            continue

        print(f"Copy {r['filepath']} to {dst_path}")
        shutil.copy(r['filepath'], dst_path)
    print("Done!")

def move_checkpoints(filenames, list, src):
    dst_dir = filer_models.get_dst_dir(src)
    for r in list:
        if r['filename'] not in filenames.split(','):
            continue

        dst_path = os.path.join(dst_dir, r['filename'])
        
        if os.path.exists(dst_path):
            print(f"Already exists: {dst_path}")
            continue

        print(f"Move {r['filepath']} to {dst_path}")
        shutil.move(r['filepath'], dst_path)
    print("Done!")

def delete_checkpoints(filenames, list):
    for r in list:
        if r['filename'] not in filenames.split(','):
            continue

        if not os.path.exists(r['filepath']):
            print(f"Not Exists: {r['filepath']}")
            continue

        print(f"Delete: {r['filepath']}")
        os.remove(r['filepath'])
    print("Done!")
