import os
import pathlib
import pprint

import gradio as gr

from modules import script_callbacks, sd_models, shared
import filer.models as filer_models
import filer.actions as filer_actions
import filer.checkpoints as filer_checkpoints
import filer.hypernetworks as filer_hypernetworks
import filer.extensions as filer_extensions
import filer.images as filer_images
import filer.dreambooths as filer_dreambooths
import filer.loras as filer_loras
import filer.files as filer_files

def js_only():
    pass

# copy begin
def copy_checkpoints_active(filenames):
    filer_actions.copy(filenames, filer_checkpoints.list_active(), filer_models.load_backup_dir('checkpoints'))
    return table_checkpoints_active()

def copy_checkpoints_backup(filenames):
    filer_actions.copy(filenames, filer_checkpoints.list_backup(), filer_checkpoints.load_active_dir())
    return table_checkpoints_backup()

def move_checkpoints_active(filenames):
    filer_actions.move(filenames, filer_checkpoints.list_active(), filer_models.load_backup_dir('checkpoints'))
    return table_checkpoints_active()

def move_checkpoints_backup(filenames):
    filer_actions.move(filenames, filer_checkpoints.list_backup(), filer_checkpoints.load_active_dir())
    return table_checkpoints_backup()

def delete_checkpoints_active(filenames):
    filer_actions.delete(filenames, filer_checkpoints.list_active())
    return table_checkpoints_active()

def delete_checkpoints_backup(filenames):
    filer_actions.delete(filenames, filer_checkpoints.list_backup())
    return table_checkpoints_backup()

def calc_checkpoints_active(filenames):
    filer_actions.calc_sha256(filenames, filer_checkpoints.list_active())
    return table_checkpoints_active()

def calc_checkpoints_backup(filenames):
    filer_actions.calc_sha256(filenames, filer_checkpoints.list_backup())
    return table_checkpoints_backup()

def save_checkpoints(data):
    filer_models.save_comment('checkpoints', data)
    return 'saved.'

def download_checkpoints_active(filenames):
    return filer_actions.download(filenames, filer_checkpoints.list_active())

def download_checkpoints_backup(filenames):
    return filer_actions.download(filenames, filer_checkpoints.list_backup())

def upload_checkpoints_active(files):
    return filer_actions.upload(files, filer_checkpoints.load_active_dir())

def upload_checkpoints_backup(files):
    return filer_actions.upload(files, filer_models.load_backup_dir())

def calc_checkpoints_backup(filenames):
    filer_actions.calc_sha256(filenames, filer_checkpoints.list_backup())
    return table_checkpoints_backup()

def table_checkpoints_active():
    return filer_checkpoints.table('checkpoints_active', filer_checkpoints.list_active())

def table_checkpoints_backup():
    return filer_checkpoints.table('checkpoints_backup', filer_checkpoints.list_backup())
# copy end

# paste
def copy_hypernetworks_active(filenames):
    filer_actions.copy(filenames, filer_hypernetworks.list_active(), filer_models.load_backup_dir('hypernetworks'))
    return table_hypernetworks_active()

def copy_hypernetworks_backup(filenames):
    filer_actions.copy(filenames, filer_hypernetworks.list_backup(), filer_hypernetworks.load_active_dir())
    return table_hypernetworks_backup()

def move_hypernetworks_active(filenames):
    filer_actions.move(filenames, filer_hypernetworks.list_active(), filer_models.load_backup_dir('hypernetworks'))
    return table_hypernetworks_active()

def move_hypernetworks_backup(filenames):
    filer_actions.move(filenames, filer_hypernetworks.list_backup(), filer_hypernetworks.load_active_dir())
    return table_hypernetworks_backup()

def delete_hypernetworks_active(filenames):
    filer_actions.delete(filenames, filer_hypernetworks.list_active())
    return table_hypernetworks_active()

def delete_hypernetworks_backup(filenames):
    filer_actions.delete(filenames, filer_hypernetworks.list_backup())
    return table_hypernetworks_backup()

def download_hypernetworks_active(filenames):
    return filer_actions.download(filenames, filer_hypernetworks.list_active())

def download_hypernetworks_backup(filenames):
    return filer_actions.download(filenames, filer_hypernetworks.list_backup())

def upload_hypernetworks_active(files):
    return filer_actions.upload(files, filer_hypernetworks.load_active_dir())

def upload_hypernetworks_backup(files):
    return filer_actions.upload(files, filer_models.load_backup_dir())

def calc_hypernetworks_active(filenames):
    filer_actions.calc_sha256(filenames, filer_hypernetworks.list_active())
    return table_hypernetworks_active()

def calc_hypernetworks_backup(filenames):
    filer_actions.calc_sha256(filenames, filer_hypernetworks.list_backup())
    return table_hypernetworks_backup()

def save_hypernetworks(data):
    filer_models.save_comment('hypernetworks', data)
    return 'saved.'

def table_hypernetworks_active():
    return filer_hypernetworks.table('hypernetworks_active', filer_hypernetworks.list_active())

def table_hypernetworks_backup():
    return filer_hypernetworks.table('hypernetworks_backup', filer_hypernetworks.list_backup())
#
def copy_extensions_active(filenames):
    filer_actions.copy(filenames, filer_extensions.list_active(), filer_models.load_backup_dir('extensions'))
    return table_extensions_active()

def copy_extensions_backup(filenames):
    filer_actions.copy(filenames, filer_extensions.list_backup(), filer_extensions.load_active_dir())
    return table_extensions_backup()

def move_extensions_active(filenames):
    filer_actions.move(filenames, filer_extensions.list_active(), filer_models.load_backup_dir('extensions'))
    return table_extensions_active()

def move_extensions_backup(filenames):
    filer_actions.move(filenames, filer_extensions.list_backup(), filer_extensions.load_active_dir())
    return table_extensions_backup()

def delete_extensions_active(filenames):
    filer_actions.delete(filenames, filer_extensions.list_active())
    return table_extensions_active()

def delete_extensions_backup(filenames):
    filer_actions.delete(filenames, filer_extensions.list_backup())
    return table_extensions_backup()

def download_extensions_active(filenames):
    return filer_actions.download(filenames, filer_extensions.list_active())

def download_extensions_backup(filenames):
    return filer_actions.download(filenames, filer_extensions.list_backup())

def upload_extensions_active(files):
    return filer_actions.upload(files, filer_extensions.load_active_dir(), True)

def upload_extensions_backup(files):
    return filer_actions.upload(files, filer_models.load_backup_dir(), True)

def calc_extensions_active(filenames):
    filer_actions.calc_sha256(filenames, filer_extensions.list_active())
    return table_extensions_active()

def calc_extensions_backup(filenames):
    filer_actions.calc_sha256(filenames, filer_extensions.list_backup())
    return table_extensions_backup()

def save_extensions(data):
    filer_models.save_comment('extensions', data)
    return 'saved.'

def table_extensions_active():
    return filer_extensions.table('extensions_active', filer_extensions.list_active())

def table_extensions_backup():
    return filer_extensions.table('extensions_backup', filer_extensions.list_backup())
#
def copy_images_active(filenames):
    filer_actions.copy(filenames, filer_images.list_active(), filer_models.load_backup_dir('images'))
    return table_images_active()

def copy_images_backup(filenames):
    filer_actions.copy(filenames, filer_images.list_backup(), filer_images.load_active_dir())
    return table_images_backup()

def move_images_active(filenames):
    filer_actions.move(filenames, filer_images.list_active(), filer_models.load_backup_dir('images'))
    return table_images_active()

def move_images_backup(filenames):
    filer_actions.move(filenames, filer_images.list_backup(), filer_images.load_active_dir())
    return table_images_backup()

def delete_images_active(filenames):
    filer_actions.delete(filenames, filer_images.list_active())
    return table_images_active()

def delete_images_backup(filenames):
    filer_actions.delete(filenames, filer_images.list_backup())
    return table_images_backup()

def download_images_active(filenames):
    return filer_actions.download(filenames, filer_images.list_active())

def download_images_backup(filenames):
    return filer_actions.download(filenames, filer_images.list_backup())

def upload_images_active(files):
    return filer_actions.upload(files, filer_images.load_active_dir(), True)

def upload_images_backup(files):
    return filer_actions.upload(files, filer_models.load_backup_dir(), True)

def calc_images_active(filenames):
    filer_actions.calc_sha256(filenames, filer_images.list_active())
    return table_images_active()

def calc_images_backup(filenames):
    filer_actions.calc_sha256(filenames, filer_images.list_backup())
    return table_images_backup()

def save_images(data):
    filer_models.save_comment('images', data)
    return 'saved.'

def table_images_active():
    return filer_images.table('images_active', filer_images.list_active())

def table_images_backup():
    return filer_images.table('images_backup', filer_images.list_backup())
#
def copy_dreambooths_active(filenames):
    filer_actions.copy(filenames, filer_dreambooths.list_active(), filer_models.load_backup_dir('dreambooths'))
    return table_dreambooths_active()

def copy_dreambooths_backup(filenames):
    filer_actions.copy(filenames, filer_dreambooths.list_backup(), filer_dreambooths.load_active_dir())
    return table_dreambooths_backup()

def move_dreambooths_active(filenames):
    filer_actions.move(filenames, filer_dreambooths.list_active(), filer_models.load_backup_dir('dreambooths'))
    return table_dreambooths_active()

def move_dreambooths_backup(filenames):
    filer_actions.move(filenames, filer_dreambooths.list_backup(), filer_dreambooths.load_active_dir())
    return table_dreambooths_backup()

def delete_dreambooths_active(filenames):
    filer_actions.delete(filenames, filer_dreambooths.list_active())
    return table_dreambooths_active()

def delete_dreambooths_backup(filenames):
    filer_actions.delete(filenames, filer_dreambooths.list_backup())
    return table_dreambooths_backup()

def calc_dreambooths_active(filenames):
    filer_actions.calc_sha256(filenames, filer_dreambooths.list_active())
    return table_dreambooths_active()

def calc_dreambooths_backup(filenames):
    filer_actions.calc_sha256(filenames, filer_dreambooths.list_backup())
    return table_dreambooths_backup()

def save_dreambooths(data):
    filer_models.save_comment('dreambooths', data)
    return 'saved.'

def download_dreambooths_active(filenames):
    return filer_actions.download(filenames, filer_dreambooths.list_active())

def download_dreambooths_backup(filenames):
    return filer_actions.download(filenames, filer_dreambooths.list_backup())

def upload_dreambooths_active(files):
    return filer_actions.upload(files, filer_dreambooths.load_active_dir(), True)

def upload_dreambooths_backup(files):
    return filer_actions.upload(files, filer_models.load_backup_dir(), True)

def calc_dreambooths_backup(filenames):
    filer_actions.calc_sha256(filenames, filer_dreambooths.list_backup())
    return table_dreambooths_backup()

def table_dreambooths_active():
    return filer_dreambooths.table('dreambooths_active', filer_dreambooths.list_active())

def table_dreambooths_backup():
    return filer_dreambooths.table('dreambooths_backup', filer_dreambooths.list_backup())
#
def copy_loras_active(filenames):
    filer_actions.copy(filenames, filer_loras.list_active(), filer_models.load_backup_dir('loras'))
    return table_loras_active()

def copy_loras_backup(filenames):
    filer_actions.copy(filenames, filer_loras.list_backup(), filer_loras.load_active_dir())
    return table_loras_backup()

def move_loras_active(filenames):
    filer_actions.move(filenames, filer_loras.list_active(), filer_models.load_backup_dir('loras'))
    return table_loras_active()

def move_loras_backup(filenames):
    filer_actions.move(filenames, filer_loras.list_backup(), filer_loras.load_active_dir())
    return table_loras_backup()

def delete_loras_active(filenames):
    filer_actions.delete(filenames, filer_loras.list_active())
    return table_loras_active()

def delete_loras_backup(filenames):
    filer_actions.delete(filenames, filer_loras.list_backup())
    return table_loras_backup()

def calc_loras_active(filenames):
    filer_actions.calc_sha256(filenames, filer_loras.list_active())
    return table_loras_active()

def calc_loras_backup(filenames):
    filer_actions.calc_sha256(filenames, filer_loras.list_backup())
    return table_loras_backup()

def save_loras(data):
    filer_models.save_comment('loras', data)
    return 'saved.'

def download_loras_active(filenames):
    return filer_actions.download(filenames, filer_loras.list_active())

def download_loras_backup(filenames):
    return filer_actions.download(filenames, filer_loras.list_backup())

def upload_loras_active(files):
    return filer_actions.upload(files, filer_loras.load_active_dir())

def upload_loras_backup(files):
    return filer_actions.upload(files, filer_models.load_backup_dir())

def calc_loras_backup(filenames):
    filer_actions.calc_sha256(filenames, filer_loras.list_backup())
    return table_loras_backup()

def table_loras_active():
    return filer_loras.table('loras_active', filer_loras.list_active())

def table_loras_backup():
    return filer_loras.table('loras_backup', filer_loras.list_backup())
# paste end

def state_hypernetworks_active(title):
    html = title + '<br><pre>' + pprint.pformat(filer_hypernetworks.state('active', title)) + '</pre>'
    return html

def state_hypernetworks_backup(title):
    html = title + '<br><pre>' + pprint.pformat(filer_hypernetworks.state('backup', title)) + '</pre>'
    return html

def make_checkpoints_active(filenames):
    html = '<pre>' + filer_checkpoints.make_yaml(filenames, filer_checkpoints.list_active()) + '</pre>'
    return html

def make_checkpoints_backup(filenames):
    html = '<pre>' + filer_checkpoints.make_yaml(filenames, filer_checkpoints.list_backup()) + '</pre>'
    return html

def convert_checkpoints_active(filenames):
    filer_checkpoints.convert_safetensors(filenames, filer_checkpoints.list_active())
    return table_checkpoints_active()

def convert_checkpoints_backup(filenames):
    filer_checkpoints.convert_safetensors(filenames, filer_checkpoints.list_backup())
    return table_checkpoints_backup()

def check_backup_dir():
    settings = filer_models.load_settings()
    html = ''
    if not settings['backup_dir']:
        html = 'First open the Settings tab and enter the backup directory'
    return html

def save_settings(*input_settings):
    return filer_models.save_settings(*input_settings)

elms = {}
def ui_set(tab1, tab2):
    global elms, out_html

    if not tab1 in elms:
        elms[tab1] = {}
    if not tab2 in elms[tab1]:
        elms[tab1][tab2] = {}

    with gr.Row():
        elms[tab1][tab2]['reload'] = gr.Button("Reload")
        elms[tab1][tab2]['select_all'] = gr.Button("Select All")
        elms[tab1][tab2]['deselect_all'] = gr.Button("Deselect All")
        elms[tab1][tab2]['save'] = gr.Button("Save comments")
    with gr.Row():
        elms[tab1][tab2]['selected'] = gr.Textbox(
            elem_id=f"filer_{tab1.lower()}_{tab2.lower()}_selected",
            label='Selected',
            lines=1,
            interactive=False
        )
    with gr.Row():
        if tab1 == 'Checkpoints':
            elms[tab1][tab2]['invokeai'] = gr.Button("Make InvokeAI models.yaml")
            elms[tab1][tab2]['safetensors'] = gr.Button("Convert to safetensors")
        if tab1 in ['Checkpoints', 'Hypernetworks', 'Loras']:
            elms[tab1][tab2]['calc_sha256'] = gr.Button("Calc SHA256")
        elms[tab1][tab2]['copy'] = gr.Button("Copy")
        elms[tab1][tab2]['move'] = gr.Button("Move")
        elms[tab1][tab2]['delete'] = gr.Button("Delete")
        elms[tab1][tab2]['download'] = gr.Button("Download")
    with gr.Row():
        elms[tab1][tab2]['table'] = gr.HTML()
    with gr.Row():
        elms[tab1][tab2]['files'] = gr.Files(interactive=True)

    elms[tab1][tab2]['save'].click(
        fn=globals()[f"save_{tab1.lower()}"],
        _js=f"save_{tab1.lower()}_{tab2.lower()}",
        inputs=[elms[tab1][tab2]['selected']],
        outputs=[out_html],
    )

    elms[tab1][tab2]['download'].click(
        fn=globals()[f"download_{tab1.lower()}_{tab2.lower()}"],
        _js=f"rows_{tab1.lower()}_{tab2.lower()}",
        inputs=[elms[tab1][tab2]['selected']],
        outputs=[elms[tab1][tab2]['files']],
    )

    elms[tab1][tab2]['files'].upload(
        fn=globals()[f"upload_{tab1.lower()}_{tab2.lower()}"],
        inputs=[elms[tab1][tab2]['files']],
        outputs=[elms[tab1][tab2]['table']],
    )

    if tab1 in ['Checkpoints', 'Hypernetworks'] and tab2 == 'Active':
        elms[tab1][tab2]['reload'].click(
            fn=globals()[f"table_{tab1.lower()}_{tab2.lower()}"],
            _js=f"reload_{tab1.lower()}",
            inputs=[],
            outputs=[elms[tab1][tab2]['table']],
        )
    else:
        elms[tab1][tab2]['reload'].click(
            fn=globals()[f"table_{tab1.lower()}_{tab2.lower()}"],
            inputs=[],
            outputs=[elms[tab1][tab2]['table']],
        )

    if tab1 == 'Checkpoints':
        elms[tab1][tab2]['invokeai'].click(
            fn=globals()[f"make_{tab1.lower()}_{tab2.lower()}"],
            _js=f"rows_{tab1.lower()}_{tab2.lower()}",
            inputs=[elms[tab1][tab2]['selected']],
            outputs=[elms[tab1][tab2]['table']],
        )
        elms[tab1][tab2]['safetensors'].click(
            fn=globals()[f"convert_{tab1.lower()}_{tab2.lower()}"],
            _js=f"rows_{tab1.lower()}_{tab2.lower()}",
            inputs=[elms[tab1][tab2]['selected']],
            outputs=[elms[tab1][tab2]['table']],
        )

    if tab1 in ['Checkpoints', 'Hypernetworks', 'Loras']:
        elms[tab1][tab2]['calc_sha256'].click(
            fn=globals()[f"calc_{tab1.lower()}_{tab2.lower()}"],
            _js=f"rows_{tab1.lower()}_{tab2.lower()}",
            inputs=[elms[tab1][tab2]['selected']],
            outputs=[elms[tab1][tab2]['table']],
        )

    if tab1 == 'Hypernetworks':
        elms[tab1][tab2]['title'] = gr.Text(elem_id=f"{tab1.lower()}_{tab2.lower()}_title", visible=False).style(container=False)
        elms[tab1][tab2]['state'] = gr.Button(elem_id=f"state_{tab1.lower()}_{tab2.lower()}_button", visible=False).style(container=False)
        elms[tab1][tab2]['state'].click(
            fn=globals()[f"state_{tab1.lower()}_{tab2.lower()}"],
            inputs=[elms[tab1][tab2]['title']],
            outputs=[out_html],
        )

    elms[tab1][tab2]['copy'].click(
        fn=globals()[f"copy_{tab1.lower()}_{tab2.lower()}"],
        _js=f"rows_{tab1.lower()}_{tab2.lower()}",
        inputs=[elms[tab1][tab2]['selected']],
        outputs=[elms[tab1][tab2]['table']],
    )

    elms[tab1][tab2]['move'].click(
        fn=globals()[f"move_{tab1.lower()}_{tab2.lower()}"],
        _js=f"rows_{tab1.lower()}_{tab2.lower()}",
        inputs=[elms[tab1][tab2]['selected']],
        outputs=[elms[tab1][tab2]['table']],
    )

    elms[tab1][tab2]['delete'].click(
        fn=globals()[f"delete_{tab1.lower()}_{tab2.lower()}"],
        _js=f"rows_{tab1.lower()}_{tab2.lower()}",
        inputs=[elms[tab1][tab2]['selected']],
        outputs=[elms[tab1][tab2]['table']],
    )

    elms[tab1][tab2]['select_all'].click(fn=js_only,_js=f"select_all_{tab1.lower()}_{tab2.lower()}")
    elms[tab1][tab2]['deselect_all'].click(fn=js_only,_js=f"deselect_all_{tab1.lower()}_{tab2.lower()}")

out_html = None
def on_ui_tabs():
    global out_html
    with gr.Blocks() as filer:
        with gr.Row(equal_height=True):
            out_html = gr.HTML(check_backup_dir())
        with gr.Tabs() as tabs:
            with gr.TabItem("Checkpoints"):
                with gr.Tabs() as tabs:
                    with gr.TabItem("Active"):
                        ui_set("Checkpoints", "Active")
                    with gr.TabItem("Backup"):
                        ui_set("Checkpoints", "Backup")
            with gr.TabItem("Dreambooths"):
                with gr.Tabs() as tabs:
                    with gr.TabItem("Active"):
                        ui_set("Dreambooths", "Active")
                    with gr.TabItem("Backup"):
                        ui_set("Dreambooths", "Backup")
            with gr.TabItem("Loras"):
                with gr.Tabs() as tabs:
                    with gr.TabItem("Active"):
                        ui_set("Loras", "Active")
                    with gr.TabItem("Backup"):
                        ui_set("Loras", "Backup")
            with gr.TabItem("Hypernetworks"):
                with gr.Tabs() as tabs:
                    with gr.TabItem("Active"):
                        ui_set("Hypernetworks", "Active")
                    with gr.TabItem("Backup"):
                        ui_set("Hypernetworks", "Backup")
            with gr.TabItem("Extensions"):
                with gr.Tabs() as tabs:
                    with gr.TabItem("Active"):
                        ui_set("Extensions", "Active")
                    with gr.TabItem("Backup"):
                        ui_set("Extensions", "Backup")
            with gr.TabItem("Images"):
                with gr.Tabs() as tabs:
                    with gr.TabItem("Active"):
                        ui_set("Images", "Active")
                    with gr.TabItem("Backup"):
                        ui_set("Images", "Backup")
            with gr.TabItem("Files"):
                files_reload = gr.Button("Reload")
                files_table = gr.HTML()
                files_title = gr.Text(elem_id=f"files_title", visible=False).style(container=False)
                files_load = gr.Button(elem_id=f"load_files_button", visible=False).style(container=False)
                files_download = gr.Button(elem_id=f"download_files_button", visible=False).style(container=False)
                files_edit = gr.Textbox(lines=10,interactive=True,label='Loaded File')
                files_save = gr.Button("Save")
                files_files = gr.Files(interactive=False)
                files_reload.click(
                    fn=filer_files.table,
                    inputs=[],
                    outputs=[files_table],
                    )
                files_load.click(
                    fn=filer_files.load,
                    inputs=[files_title],
                    outputs=[files_edit],
                    )
                files_save.click(
                    fn=filer_files.save,
                    inputs=[files_title, files_edit],
                    outputs=[out_html],
                    )
                files_download.click(
                    fn=filer_files.download,
                    inputs=[files_title],
                    outputs=[files_files],
                    )

            with gr.TabItem("Settings"):
                apply_settings = gr.Button("Apply settings")
                settings = []
                for k, v in filer_models.load_settings().items():
                    with gr.Row():
                        settings.append(gr.Textbox(value=v,label=k.title()))

        apply_settings.click(
            fn=save_settings,
            inputs=settings,
            outputs=[out_html],
        )

    return (filer, "Filer", "filer"),


script_callbacks.on_ui_tabs(on_ui_tabs)
