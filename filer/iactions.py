import os
import shutil
import pathlib
import hashlib
import json
import copy
import re
import pprint
import itertools
import math
import time

from zlib import crc32
from PIL import Image, ImageDraw, ImageFont

from modules import shared
from modules.shared import opts, cmd_opts, state

from . import models as infotexts_models

default_dirs = {
    "PNG to TXT": ['png', 'txt'],
    "TXT to PNG": ['txt', 'png'],
    "TXT to JSON": ['txt', 'json'],
    "COPY TXT": ['txt', 'edit_txt'],
    "JSON to EDIT TXTs": ['json', 'edit_txt'],
    "MACRO TXT": ['edit_txt', 'edit_txt'],
    "OUTPUT to WEBP": ['output', 'webp'],
    }

def get_convert_actions():
    return list(default_dirs.keys())

def get_target_dir():
    p = pathlib.Path(__file__).parts[-4:-2]
    return os.path.join(p[0], p[1], 'infotexts', 'edit_txt')

def get_default_dir(action):
    p = pathlib.Path(__file__).parts[-4:-2]
    for k, d in default_dirs.items():
        if action == k:
            return [os.path.join(p[0], p[1], 'infotexts', d[0]), os.path.join(p[0], p[1], 'infotexts', d[1])]
    return ['', '']

def convert(action, input_dir, output_dir):
    if not os.path.exists(input_dir):
        return f"Not exists input_dir: {input_dir}"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not action:
        return f"Please Select action."
    elif action == "PNG to TXT":
        return convert_png_to_txt(input_dir, output_dir)
    elif action == "TXT to PNG":
        return convert_txt_to_png(input_dir, output_dir)
    elif action == "TXT to JSON":
        return convert_txt_to_json(input_dir, output_dir)
    elif action == "COPY TXT":
        return copy_txt(input_dir, output_dir)
    elif action == "JSON to EDIT TXTs":
        return convert_json_to_txts(input_dir, output_dir)
    elif action == "MACRO TXT":
        return macro_txt(input_dir, output_dir)
    elif action == "OUTPUT to WEBP":
        return convert_png_to_webp(input_dir, output_dir)

    return f"Invalid action: {action}"

def convert_png_to_txt(input_dir, output_dir):
    i = 0
    # ディレクトリ内のすべてのpngファイルを検索する
    for filename in os.listdir(input_dir):
        if not filename.endswith('.png'):
            continue
        # ファイルパスを作成する
        filepath = os.path.join(input_dir, filename)

        # pngファイルを開く
        img = Image.open(filepath)

        # pngファイルからtEXtチャンクを検索する
        if img.text['parameters']:
            # tEXtチャンクのパラメータを取得する
            chunk_parameters = img.text['parameters']

            dst_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.txt')

            # tEXtチャンクの内容を出力する
            with open(dst_path, 'w', encoding='utf-8', newline='\n') as txt_file:
                txt_file.write(chunk_parameters)
                i += 1
    return f"output {i} files."

def convert_txt_to_png(input_dir, output_dir):
    def tEXt(key: str, val: str) -> bytes:
        str = key + "\0" + val
        return (len(str)).to_bytes(4, 'big') + b'tEXt' + str.encode() + (crc32(b'tEXt' + str.encode())).to_bytes(4, 'big')

    i = 0
    for filename in os.listdir(input_dir):
        if not filename.endswith('.txt'):
            continue
        # ファイルパスを作成する
        filepath = os.path.join(input_dir, filename)
        dst_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.png')

        # parametersを読みとる
        with open(filepath, 'r') as f:
            txt = f.read()
            text = tEXt('parameters', txt)
        if not text:
            continue

        # 1x1のPNGを作る
        im = Image.new('RGB', (1, 1))
        im.save(dst_path)

        # PNGファイルをバイナリとして開く
        with open(dst_path, 'r+b') as f:
            png = f.read()

        # PNGにparametersを埋め込む
        iend = bytes.fromhex('0000000049454e44ae426082')
        png = png.replace(iend, text + iend)

        # PNGを書き込む
        with open(dst_path, 'w+b') as f:
            f.write(png)
            i += 1
    return f"output {i} files."

def convert_txt_to_json(input_dir, output_dir):
    i = 0
    for filename in os.listdir(input_dir):
        if not filename.endswith('.txt'):
            continue
        # ファイルパスを作成する
        filepath = os.path.join(input_dir, filename)
        dst_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.json')

        # parametersをdictに格納する
        params = infotexts_models.txt_to_dict(filepath)

        # jsonを書き込む
        with open(dst_path, 'w') as f:
            json.dump(params, f, indent=4)
            i += 1
    return f"output {i} files."

def copy_txt(input_dir, output_dir):
    i = 0
    for filename in os.listdir(input_dir):
        if not filename.endswith('.txt'):
            continue
        # ファイルパスを作成する
        filepath = os.path.join(input_dir, filename)
        dst_path = os.path.join(output_dir, filename)

        shutil.copy(filepath, dst_path)
        i += 1
    return f"output {i} files."

def convert_json_to_txts(input_dir, output_dir):
    def shift_attention(text, distance):
        re_attention_span = re.compile(r"([.\d]+)~([.\d]+)", re.X)
        def inject_value(distance, match_obj):
            start_weight = float(match_obj.group(1))
            end_weight = float(match_obj.group(2))
            return str(round(start_weight + (end_weight - start_weight) * distance, 6))

        res = re.sub(re_attention_span, lambda match_obj: inject_value(distance, match_obj), text)
        return res

    input_files = 0
    output_files = 0
    for filename in os.listdir(input_dir):
        if not filename.endswith('.json'):
            continue
        # ファイルパスを作成する
        filepath = os.path.join(input_dir, filename)
        dst_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.txt')

        with open(filepath) as f:
            data = json.load(f)

            # prompt_countは事前に処理する
            if ("prompt_count" in data):
                c = data["prompt_count"]
                if c > 1:
                    p = []
                    for i in range(c):
                        res = shift_attention(data["prompt"], float(i / (c - 1)))
                        p.append(res)
                        if (res == data["prompt"]):
                            break
                    data["prompt"] = p
                    p = []
                    for i in range(c):
                        res = shift_attention(data["negative_prompt"], float(i / (c - 1)))
                        p.append(res)
                        if (res == data["negative_prompt"]):
                            break
                    data["negative_prompt"] = p
                del data["prompt_count"]

            tmp = []
            # 辞書のitemで回す
            for key, value in data.items():
                if type(value) != list:
                    # valueがリストでないときはリストに変換
                    # リストの要素がstrでないときはstrに変換してtmpに突っ込む
                    tmp.append([str(data[key])] if data[key] != str else [data[key]])
                else:
                    # valueがリスト
                    # valueの要素のsub_keyがstrでないときはstrに変換
                    tmp.append( [str(sub_key) if sub_key != str else sub_key for sub_key in value] )

            # *tmp でリストを展開して突っ込む ここで項目が1要素でもリストにしておかないと文字列のリストとみなされる
            result = list(itertools.product(*tmp, repeat=1))
            # pprint.pprint(result)
            jobs = []
            for r in result:
                i = 0
                job = dict()
                for k in data.keys():
                    job.update({k.lower(): r[i]})
                    i += 1
                jobs.append(job.copy())
            i = 0
            for job in jobs:
                dst_path = os.path.join(output_dir, os.path.splitext(filename)[0] + f"-{str(i).zfill(5)}.txt")
                text = infotexts_models.dict_to_text(job, True)
                with open(dst_path, 'w') as f:
                    f.write(text)
                i += 1
                output_files += 1
        input_files += 1
    return f"input {input_files} output {output_files} files."

def macro_txt(input_dir, output_dir):
    macros = []
    p = pathlib.Path(__file__).parts[-4:-2]
    macro_path = os.path.join(p[0], p[1], 'config', 'macro.txt')
    if os.path.exists(macro_path):
        with open(macro_path, 'r') as f:
            for line in f:
                macros.append(line.rstrip("\r\n").split("\t"))
    if not macros:
        return "macro not found."

    i = 0
    for filename in os.listdir(input_dir):
        if not filename.endswith('.txt'):
            continue
        # ファイルパスを作成する
        filepath = os.path.join(input_dir, filename)
        dst_path = os.path.join(output_dir, filename)

        text = infotexts_models.dict_to_text(macros_run(macros, infotexts_models.txt_to_dict(filepath)))
        with open(dst_path, 'w') as f:
            f.write(text)
        i += 1
    return f"output {i} files."

def upscale(image, scaler_index, resize, mode, resize_w, resize_h, crop):
    upscaler = shared.sd_upscalers[scaler_index]
    c = upscaler.scaler.upscale(image, resize, upscaler.data_path)
    if mode == 1 and crop:
        cropped = Image.new("RGB", (resize_w, resize_h))
        cropped.paste(c, box=(resize_w // 2 - c.width // 2, resize_h // 2 - c.height // 2))
        c = cropped
    return c

def convert_png_to_webp(input_dir, output_dir):
    p = pathlib.Path(__file__).parts[-4:-2]
    config_path = os.path.join(p[0], p[1], 'config', 'webp.json')

    cfg = {}
    with open(config_path) as f:
        cfg = json.load(f)

    i = 0
    for filename in os.listdir(input_dir):
        if not filename.endswith('.png'):
            continue
        # ファイルパスを作成する
        filepath = os.path.join(input_dir, filename)
        dst_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.webp')
        
        image = Image.open(filepath)
        image = image.convert("RGB")

        # webp upscale
        if ("upscaler" in cfg):
            u = 0
            for upscaler in shared.sd_upscalers:
                if upscaler.name == cfg["upscaler"]:
                    extras_upscaler_1 = u
                    break
                u += 1

            if ("upscaling_resize" in cfg):
                upscaling_resize = float(cfg["upscaling_resize"])
            if ("upscaling_resize_w" in cfg):
                upscaling_resize_w = int(cfg["upscaling_resize_w"])
            if ("upscaling_resize_h" in cfg):
                upscaling_resize_h = int(cfg["upscaling_resize_h"])
            if ("upscaling_crop" in cfg):
                upscaling_crop = bool(cfg["upscaling_crop"])

            if upscaling_resize == 1.0:
                resize_mode = 1
                upscaling_resize = max(upscaling_resize_w/image.width, upscaling_resize_h/image.height)
            else:
                resize_mode = 0
                upscaling_resize_w = image.width * upscaling_resize
                upscaling_resize_h = image.height * upscaling_resize

            image = upscale(image,
                extras_upscaler_1,
                upscaling_resize,
                resize_mode,
                upscaling_resize_w,
                upscaling_resize_h,
                upscaling_crop
                )

        # webp text
        if "draw_text" in cfg:
            font = ImageFont.truetype(
                cfg["imagefont_truetype"] if "imagefont_truetype" in cfg else 'Arial.ttf',
                index=int(cfg["imagefont_truetype_index"]) if "imagefont_truetype_index" in cfg else 0,
                size=int(cfg["imagefont_truetype_size"] if "imagefont_truetype_size" in cfg else 24)
            )

            draw = ImageDraw.Draw(image)
            draw.text((
                int(cfg["draw_text_left"]) if "draw_text_left" in cfg else 0,
                int(cfg["draw_text_top"]) if "draw_text_top" in cfg else 0,
                ), cfg["draw_text"],
                cfg["draw_text_color"] if "draw_text_color" in cfg else 'black',
                font=font
            )

        # webp save
        q = int(cfg["webp_quality"]) if "webp_quality" in cfg else 95
        image.save(dst_path, quality=q)
        i += 1
    return f"output {i} files."

def macro_add_line(macro_text, macro_target, macro_action, macro_1, macro_2):
    return f"{macro_text}{macro_target}\t{macro_action}\t{macro_1}\t{macro_2}\n".encode().decode('unicode-escape')

def macros_run(macros, data):
    for key in list(data.keys()):
        if (key != key.lower()):
            data[key.lower()] = data[key]
            del data[key]

    for macro in macros:
        if (macro[0] == 'Prompt'):
            key = 'prompt'
        elif (macro[0] == 'Negative Prompt'):
            key = 'negative_prompt'
        elif (macro[0] == 'Key'):
            key = macro[2].lower()

        if not key in data:
            print(f"data not in: {key}")
            continue

        if (macro[1] == 'Add First'):
            data[key] = macro[3] + data[key]
        elif (macro[1] == 'Add Last'):
            data[key] += macro[3]
        elif (macro[1] == 'Replace'):
            data[key] = data[key].replace(macro[2], macro[3])
        elif (macro[1] == 're.sub'):
            pattern = re.compile(macro[2])
            data[key] = pattern.sub(macro[3], data[key])
        elif (macro[1] == 'Overwrite'):
            data[key] = macro[3]
            
    return data

def macro_load():
    p = pathlib.Path(__file__).parts[-4:-2]
    filepath = os.path.join(p[0], p[1], 'config', 'macro.txt')

    text = ''
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            text = f.read()
    return [text.encode().decode('unicode-escape'), 'macro loaded.']

def macro_save(text):
    p = pathlib.Path(__file__).parts[-4:-2]
    filepath = os.path.join(p[0], p[1], 'config', 'macro.txt')

    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))
    with open(filepath, 'w') as f:
        f.write(text)
    return ['macro saved.']
