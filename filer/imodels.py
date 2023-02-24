import os
import pathlib
import json

from modules import sd_models

param_keys = [
    "model_hash",
    "hypernet",
    "model_sha256",
    "vae_sha256",
    "hypernet_sha256",
    "steps",
    "sampler",
    "cfg_scale",
    "width",
    "height",
    "seed",
    "clip_skip",
    "prompt",
    "negative_prompt",
    "hypernet_strength",
    "eta",
    "ensd",
    "subseed",
    "subseed_strength",
	"seed_resize_from_w",
    "seed_resize_from_h",
    "denoising_strength",
]

default_webp_settings = {
    "webp_quality": "90",
    "upscaler": "R-ESRGAN 2x+",
    "upscaling_resize": "2",
    "upscaling_resize_w": "0",
    "upscaling_resize_h": "0",
    "upscaling_crop": "1",
    "imagefont_truetype": "Arial.ttf",
    "imagefont_truetype_index": "0",
    "imagefont_truetype_size": "24",
    "draw_text_left": "0",
    "draw_text_top": "0",
    "draw_text_color": "Black",
    "draw_text": ""
}

default_generate_settings = {
    "input_dir": "",
    "output_dir": "",
    "ignore_keys": [],
    "webp_dir": "",
}
def load_webp_settings():
    p = pathlib.Path(__file__).parts[-4:-2]
    filepath = os.path.join(p[0], p[1], 'config', 'webp.json')
    settings = default_webp_settings
    if os.path.exists(filepath):
        with open(filepath) as f:
            settings.update(json.load(f))
    return settings

def save_webp_settings(*input_settings):
    p = pathlib.Path(__file__).parts[-4:-2]
    filepath = os.path.join(p[0], p[1], 'config', 'webp.json')
    data = {}
    if os.path.exists(filepath):
        with open(filepath) as f:
            data = json.load(f)
    i = 0
    for k in default_webp_settings.keys():
        data.update({k: input_settings[i]})
        i += 1
    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))
    with open(filepath, "w") as f:
        json.dump(data, f)
    return json.dumps(data)

def load_generate_settings():
    p = pathlib.Path(__file__).parts[-4:-2]
    filepath = os.path.join(p[0], p[1], 'config', 'generate.json')
    settings = default_generate_settings
    if os.path.exists(filepath):
        with open(filepath) as f:
            settings.update(json.load(f))
    return settings

def save_generate_settings(*input_settings):
    p = pathlib.Path(__file__).parts[-4:-2]
    filepath = os.path.join(p[0], p[1], 'config', 'generate.json')
    data = {}
    if os.path.exists(filepath):
        with open(filepath) as f:
            data = json.load(f)
    i = 0
    for k in default_generate_settings.keys():
        data.update({k: input_settings[i]})
        i += 1
    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))
    with open(filepath, "w") as f:
        json.dump(data, f)
    return json.dumps(data)

def get_list():
    p = pathlib.Path(__file__).parts[-3]

    rs = []
    for filepath in list_dirs():
        if not os.path.exists(filepath):
            continue

        filename = os.path.basename(filepath)

        r = {}

        r['title'] = filename
        r['filename'] = filename
        r['filepath'] = filepath
        r['files'] = sum(os.path.isfile(os.path.join(filepath, name)) for name in os.listdir(filepath))

        rs.append(r)

    return rs

def list_dirs():
    p = pathlib.Path(__file__).parts[-4:-2]
    dirs = [
        os.path.join(p[0], p[1], 'infotexts', 'txt'),
        os.path.join(p[0], p[1], 'infotexts', 'png'),
        os.path.join(p[0], p[1], 'infotexts', 'json'),
        os.path.join(p[0], p[1], 'infotexts', 'edit_txt'),
        os.path.join(p[0], p[1], 'infotexts', 'output'),
        os.path.join(p[0], p[1], 'infotexts', 'webp'),
    ]

    return dirs

def get_generate_input_dir():
    cfg = load_generate_settings()
    if cfg['input_dir']:
        return cfg['input_dir']

    p = pathlib.Path(__file__).parts[-4:-2]
    return os.path.join(p[0], p[1], 'infotexts', 'edit_txt')

def get_generate_output_dir(is_default = True):
    cfg = load_generate_settings()
    if cfg['output_dir']:
        return cfg['output_dir']
    if not is_default:
        return ''

    p = pathlib.Path(__file__).parts[-4:-2]
    return os.path.join(p[0], p[1], 'infotexts', 'output')

def get_generate_webp_dir(is_default = False):
    cfg = load_generate_settings()
    if cfg['webp_dir']:
        return cfg['webp_dir']
    if not is_default:
        return ''

    p = pathlib.Path(__file__).parts[-4:-2]
    return os.path.join(p[0], p[1], 'infotexts', 'webp')

def get_ignore_keys():
    cfg = load_generate_settings()
    if cfg['ignore_keys']:
        return cfg['ignore_keys']
    return []

def txt_to_dict(filepath, is_array = False):
    with open(filepath, 'r', encoding="utf-8") as f:
        text = f.read()
    try:
        import modules.generation_parameters_copypaste as parameters_copypaste
        params = parameters_copypaste.parse_generation_parameters(text)
    except:
        print(text)
        raise ValueError("edit_txt Syntax error")

    res = {}
    for k, v in params.items():
        k = k.lower().replace(' ', '_')
        if k == 'size-1':
            k = 'width'
        elif k == 'size-2':
            k = 'height'
        if is_array and k not in ['prompt', 'negative_prompt']:
            res[k] = [v]
        else:
            res[k] = v
    return res

def dict_to_text(job):
    text = ''

    if 'prompt' in job:
        text += job['prompt'] + "\n"
        del job['prompt']
    if 'negative_prompt' in job:
        text += job['negative_prompt'] + "\n"
        del job['negative_prompt']
    if 'steps' in job:
        text += f"steps: {job['steps']}, "
        del job['steps']

    pairs = []
    for k, v in job.items():
        k = k.lower()
        if k in ['prompt', 'negative_prompt']:
            continue
        pairs.append(f"{k}: {v}")
    text += f"{', '.join(pairs)}\n"

    return text

def list_html():
    rs = get_list()
    code = f"""
    <table>
        <thead>
            <tr>
                <th>name</th>
                <th>path</th>
                <th>files</th>
            </tr>
        </thead>
        <tbody>
    """

    for r in rs:
        code += f"""
            <tr class="infotexts_list_row" data-title="{r['title']}">
                <td class="infotexts_filename">{r['filename']}</td>
                <td class="infotexts_filepath">{r['filepath']}</td>
                <td class="infotexts_files">{r['files']}</td>
            </tr>
            """

    code += """
        </tbody>
    </table>
    """

    return code

