import math
import os
import sys
import traceback
import random
import json
import platform
import subprocess as sp
import copy
import re
import pprint
import itertools
import time

from PIL import Image, ImageDraw, ImageFont
from glob import glob
import gradio as gr

import modules.scripts as scripts
from modules import sd_samplers, sd_models, shared, sd_vae
from modules.processing import Processed, process_images
from modules.shared import opts, cmd_opts, state
from modules.hypernetworks import hypernetwork
from . import imodels as infotexts_models
from . import iactions as infotexts_actions
from . import sha256

# Hypernetをnameから引けるように準備しておく
def save_hn_name(filepath, is_overwrite = False):
    hn_name_path = filepath + '.name'

    if not os.path.exists(hn_name_path) or is_overwrite:
        h = hypernetwork.Hypernetwork()
        h.load(filepath)

        with open(hn_name_path, 'w') as f:
            f.write(h.name)

def list_hn_names(dir):
    if not os.path.exists(dir):
        return {}

    res = {}
    for filename in os.listdir(dir):
        if not filename.endswith('.pt'):
            continue
        filepath = os.path.join(dir, filename)
        name_name = filename + '.name'
        name_path = os.path.join(dir, name_name)

        if not os.path.exists(name_path):
            save_hn_name(filepath)
        with open(name_path, 'r') as f:
            hn_name = f.read()
        res[hn_name] = filepath
    return res

def generate_images(p):
    global opts

    input_dir = infotexts_models.get_generate_input_dir()
    output_dir = infotexts_models.get_generate_output_dir(False)
    
    cfg = infotexts_models.load_generate_settings()

    jobs = []
    for filename in os.listdir(input_dir):
        if not filename.endswith('.txt'):
            continue
        filepath = os.path.join(input_dir, filename)
        data = infotexts_models.txt_to_dict(filepath)
        job = dict()
        job.update({"filename": os.path.splitext(filename)[0]})

        # 厳密な型変換
        for k, v in data.items():
            k = k.lower()

            # 無視するキー(txt2imgの入力を使う)
            if k in cfg['ignore_keys']:
                continue
            
            if k in ["width","height","steps","clip_skip","ensd","subseed","seed_resize_from_w","seed_resize_from_h"]:
                job.update({k: int(v)})
            elif k in ["cfg_scale","hypernet_strength", "eta","subseed_strength","denoising_strength"]:
                job.update({k: float(v)})
            elif k == "sd_model_hash":
                job.update({"model_hash": v})
            elif k == "sampler":
                job.update({"sampler_name": v})
            else:
                job.update({k: v})
        jobs.append(job.copy())

    img_count = len(jobs) * p.n_iter
    batch_count = math.ceil(img_count / p.batch_size)
    print(f"Will process {img_count} images in {batch_count} batches.")

    state.job_count = batch_count

    original_opts = copy.copy(opts)

    for c in sd_models.checkpoints_list.values():
        ckpt_dir = os.path.dirname(c.filename)
        break
    ckpt_sha256s = sha256.list_sha256(ckpt_dir, ['ckpt', 'safetensors'])
    vae_sha256s = sha256.list_sha256(ckpt_dir, ['vae.pt'])
    hypernet_sha256s = sha256.list_sha256(cmd_opts.hypernetwork_dir, ['pt'])
    hypernet_names = list_hn_names(cmd_opts.hypernetwork_dir)

    opts.save_images_add_number = False

    images = []
    for i, job in enumerate(jobs):
        copy_p = copy.copy(p)
        copy_p.outpath_samples = output_dir
        state.job = f"{i + 1} out of {state.job_count}"

        # 値の指定が無いものは任意ではなく、以下の値が指定されているものとみなす
        opts.eta_noise_seed_delta = 0
#        opts.sd_hypernetwork_strength = 1.0
        opts.eta_ddim = 0.0
        opts.eta_ancestral = 1.0

        for k, v in job.items():
            if k == "filename":
                opts.samples_filename_pattern = v
            elif k == "model_hash":
                if "model_sha256" in job.keys():
                    continue
                for c in sd_models.checkpoints_list.values():
                    if c.hash == v:
                        copy_p.override_settings['sd_model_checkpoint'] = c.title
#            elif k == "hypernet":
#                if "hypernet_sha256" in job.keys():
#                    continue
#                if v == "None":
#                    opts.sd_hypernetwork = None
#                    continue
#                if shared.loaded_hypernetwork != None and shared.loaded_hypernetwork.name == v:
#                    continue
#                if not v in hypernet_names.keys():
#                    continue
#                path = hypernet_names[v]
#                shared.loaded_hypernetwork = hypernetwork.Hypernetwork()
#                shared.loaded_hypernetwork.load(path)
            elif k == "model_sha256":
                path = sha256.match_sha256(v, ckpt_sha256s)
                if not path:
                    continue
                for c in sd_models.checkpoints_list.values():
                    if c.filename == path:
                        if "vae_sha256" in job.keys():
                            vae_file = sha256.match_sha256(job['vae_sha256'], vae_sha256s)
                        else:
                            vae_file="auto"
                        sd_models.load_model_weights(shared.sd_model, c, vae_file=vae_file)
            elif k == "vae_sha256":
                pass
#            elif k == "hypernet_sha256":
#                path = sha256.match_sha256(v, hypernet_sha256s)
#                if not path:
#                    continue
#                shared.loaded_hypernetwork = hypernetwork.Hypernetwork()
#                shared.loaded_hypernetwork.load(path)
#            elif k == "hypernet_strength":
#                opts.sd_hypernetwork_strength = float(v)
            elif k == "ensd":
                opts.eta_noise_seed_delta = v
            else:
                setattr(copy_p, k, v)

        proc = process_images(copy_p)
        images += proc.images

    # 変えた設定を元に戻す
    opts.save_images_add_number = original_opts.save_images_add_number
    opts.eta_noise_seed_delta = original_opts.eta_noise_seed_delta
#    opts.sd_hypernetwork = original_opts.sd_hypernetwork
#    opts.sd_hypernetwork_strength = original_opts.sd_hypernetwork_strength
    opts.eta_ddim = original_opts.eta_ddim
    opts.eta_ancestral = original_opts.eta_ancestral
    opts.samples_filename_pattern = original_opts.samples_filename_pattern

    # webp出力先ディレクトリが指定されていれば、ついでにwebpにする
    webp_dir = infotexts_models.get_generate_webp_dir(False)
    if webp_dir:
        infotexts_actions.convert_png_to_webp(output_dir, webp_dir)

    return images
