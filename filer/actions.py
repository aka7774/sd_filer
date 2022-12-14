import os
import shutil
import pathlib
import hashlib
import requests

from . import models as filer_models
from . import images as filer_images

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
        if r['title'] not in filenames.split(','):
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
        if r['title'] not in filenames.split(','):
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
            if (os.path.exists(r['filepath'] + '.sha256')):
                try:
                    shutil.copy(r['filepath'] + '.sha256', dst_path + '.sha256')
                except:
                    pass
            if (os.path.exists(os.path.splitext(r['filepath'])[0] + '.yaml')):
                try:
                    shutil.copy(os.path.splitext(r['filepath'])[0] + '.yaml', os.path.splitext(dst_path)[0] + '.yaml')
                except:
                    pass
    print("Copy Done!")

def move(filenames, list, dst_dir):
    if not dst_dir:
        raise ValueError('Please Input Backup Directory')
        return
    
    for r in list:
        if r['title'] not in filenames.split(','):
            continue

        dst_path = os.path.join(dst_dir, r['filename'])
        
        if os.path.exists(dst_path):
            print(f"Already exists: {dst_path}")
            continue

        print(f"Move {r['filepath']} to {dst_path}")
        shutil.move(r['filepath'], dst_path)
        if (os.path.exists(r['filepath'] + '.sha256')):
            try:
                shutil.move(r['filepath'] + '.sha256', dst_path + '.sha256')
            except:
                pass
            if (os.path.exists(os.path.splitext(r['filepath'])[0] + '.yaml')):
                try:
                    shutil.move(os.path.splitext(r['filepath'])[0] + '.yaml', os.path.splitext(dst_path)[0] + '.yaml')
                except:
                    pass
    print("Move Done!")

def delete(filenames, list):
    for r in list:
        if r['title'] not in filenames.split(','):
            continue

        if not os.path.exists(r['filepath']):
            print(f"Not Exists: {r['filepath']}")
            continue

        print(f"Delete: {r['filepath']}")
        if os.path.isdir(r['filepath']):
            shutil.rmtree(r['filepath'])
        else:
            os.remove(r['filepath'])
            if (os.path.exists(r['filepath'] + '.sha256')):
                try:
                    os.remove(r['filepath'] + '.sha256')
                except:
                    pass
            if (os.path.exists(os.path.splitext(r['filepath'])[0] + '.yaml')):
                try:
                    os.remove(os.path.splitext(r['filepath'])[0] + '.yaml')
                except:
                    pass
    print("Delete Done!")

def download(filenames, list):
    files = []
    for r in list:
        if r['title'] not in filenames.split(','):
            continue

        if os.path.isdir(r['filepath']):
            zip_path = shutil.make_archive(r['filename'], 'zip', root_dir=r['filepath'])
            files.append(zip_path)
        else:
            files.append(r['filepath']) 
    print("Download prepare Done! (Link is below)")
    return files

def upload(files, dir, is_zip = False):
    # アップロードされたファイルはtmpに存在する
    for file in files:
        tmp_stem, ext = os.path.splitext(os.path.basename(file.name))
        
        # zipモードの時は展開する
        if is_zip:
            if ext != '.zip':
                raise ValueError("Only upload zip.")
                continue
            filename = tmp_stem[:-8]
            filepath = os.path.join(dir, filename)
            if os.path.exists(filepath):
                print(f"Already exists: {filepath}")
                continue
            shutil.unpack_archive(file.name, filepath)
            # imagesの時は一覧への追加を試みる
            if not dir:
                filer_images.list_append(filename)
        else:
            # アップロードされたファイル名の末尾には8桁のランダム文字列が付与されている
            filename = tmp_stem[:-8] + ext
            filepath = os.path.join(dir, filename)

            if os.path.exists(filepath):
                print(f"Already exists: {filepath}")
                continue
            shutil.copy(file.name, filepath)
    print("Upload Done!")

def urls(urls, dst_dir):
    for url in urls.split("\n"):
        url = url.rstrip("\r")
        filename = os.path.basename(url)
        dst_path = os.path.join(dst_dir, filename)
        if os.path.exists(dst_path):
            raise ValueError(f"{dst_path} Already exists.")
        print(f"Downloading {url}")
        res = requests.get(url, stream=True)
        if res.status_code == 200:
            size = res.headers.get('content-length', -1)
            print(f"Content-Length: {size}")
            with open(dst_path, 'wb') as f:
                for chunk in res.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()
                print(f"Done.")
