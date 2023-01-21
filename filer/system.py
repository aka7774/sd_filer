import os
import sys
import platform
import shutil
import datetime
import torch

import importlib.util
if sys.version_info < (3, 8):
    import importlib_metadata
else:
    import importlib.metadata as importlib_metadata

import gradio as gr

from launch import run
from modules import script_callbacks, sd_models, shared, extensions

def print_about_basic():
    rs = []

    try:
        rs.append(f"Reported at {datetime.datetime.now()} by github.com/aka7774/sd_filer")
    except:
        rs.append(f"Reported by github.com/aka7774/sd_filer")

    try:
        rs.append(f"Python {sys.version}")
    except:
        rs.append(f"Python: unknown")

    try:
        free, total = torch.cuda.mem_get_info()
        rs.append(f"GPU {torch.cuda.get_device_name()}, VRAM: {gib(total)} GiB")
    except:
        rs.append(f"GPU: unknown")

    rs.append(f'argv: {" ".join(sys.argv[1:])}')

    try:
        git = os.environ.get('GIT', "git")
        commithash = run(f"{git} rev-parse HEAD").strip()
        rs.append('stable-diffusion-webui: ' + commithash)
    except:
        pass

    checks = ["bitsandbytes", "diffusers", "transformers", "xformers", "torch", "torchvision"]
    for check in checks:
        check_ver = "N/A"
        try:
            check_available = importlib.util.find_spec(check) is not None
            if check_available:
                check_ver = importlib_metadata.version(check)
        except importlib_metadata.PackageNotFoundError:
            check_available = False
        if check_available:
            rs.append(f"{check}: {check_ver}")
        else:
            rs.append(f"{check}: NOT installed.")

    return "\n".join(rs)

def print_about_detail():
    rs = []

    try:
        rs.append(f"Reported at {datetime.datetime.now()} by github.com/aka7774/sd_filer")
    except:
        rs.append(f"Reported by github.com/aka7774/sd_filer")

    try:
        rs.append(f"{platform.system()} ({platform.platform()})")
    except:
        rs.append(f"platform: unknown")

    try:
        rs.append(f"{platform.machine()} ({platform.processor()})")
    except:
        rs.append(f"processor: unknown")

    try:
        # Windowsでは取れない
        mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
        rs.append(f'Memory total: {gib(mem_bytes)} GiB')
    except:
        try:
            import psutil
            mem = psutil.virtual_memory()
            rs.append(f'Memory: {gib(mem.total)} GiB')
        except:
            rs.append('Memory: unknown')

    try:
        total, used, free = shutil.disk_usage(os.path.abspath('.'))
        rs.append(f"Disk: {gib(total - free)} / {gib(total)} GiB")
    except:
        rs.append('Disk: unknown')

    rs.append('')

    try:
        git = os.environ.get('GIT', "git")
        for ext in extensions.extensions:
            if ext.is_builtin or not ext.enabled:
                continue
            commithash = run(f"{git} -C {os.path.abspath(ext.path)} rev-parse HEAD").strip()
            rs.append(f"{ext.name}: {commithash}")
    except:
        rs.append('Extensions: unknown')

    return "\n".join(rs)

def get_commithash(url):
    try:
        import requests
        commits = requests.get(url).json()
        return commits['commit']['sha']
    except Exception as e:
        return 'failed'

def gib(bytes):
    return round(bytes / (2**30), 2)
