import os
import shutil
import pathlib
import hashlib

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

def calc_sha256(filenames, list):
    for r in list:
        if r['filename'] not in filenames.split(','):
            continue

        r['sha256'] = calc_hash('sha256', r['filepath'])
        pathlib.Path(r['sha256_path']).write_text(r['sha256'], encoding="utf-8")
        print(f"{r['filepath']} sha256: {r['sha256']}")
    print("Done!")

def copy(filenames, list, dst_dir):
    if not dst_dir:
        raise ValueError('Please Input Backup Directory')
        return

    for r in list:
        if r['filename'] not in filenames.split(','):
            continue

        dst_path = os.path.join(dst_dir, r['filename'])
        
        if os.path.exists(dst_path):
            print(f"Already exists: {dst_path}")
            continue

        print(f"Copy {r['filepath']} to {dst_path}")
        if os.path.isdir(r['filepath']):
            shutil.copytree(r['filepath'], dst_path)
        else:
            shutil.copy(r['filepath'], dst_path)
    print("Done!")

def move(filenames, list, dst_dir):
    if not dst_dir:
        raise ValueError('Please Input Backup Directory')
        return
    
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

def delete(filenames, list):
    for r in list:
        if r['filename'] not in filenames.split(','):
            continue

        if not os.path.exists(r['filepath']):
            print(f"Not Exists: {r['filepath']}")
            continue

        print(f"Delete: {r['filepath']}")
        if os.path.isdir(r['filepath']):
            shutil.rmtree(r['filepath'])
        else:
            os.remove(r['filepath'])
    print("Done!")
