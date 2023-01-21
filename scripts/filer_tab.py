import os
import pathlib
import pprint

import gradio as gr

from modules import script_callbacks, sd_models, shared
import filer.models as filer_models
import filer.actions as filer_actions
from filer.checkpoints import FilerGroupCheckpoints
from filer.embeddings import FilerGroupEmbeddings
from filer.dreambooths import FilerGroupDreambooths
from filer.loras import FilerGroupLoras
from filer.hypernetworks import FilerGroupHypernetworks
from filer.extensions import FilerGroupExtensions
from filer.images import FilerGroupImages
from filer.files import FilerGroupFiles

def js_only():
    pass

def check_backup_dir():
    settings = filer_models.load_settings()
    html = ''
    if not settings['backup_dir']:
        html = 'First open the Settings tab and enter the backup directory'
    return html

def save_settings(*input_settings):
    return [
        filer_models.save_settings(*input_settings),
        filer_models.load_backup_dir('checkpoints'),
        filer_models.load_backup_dir('embeddings'),
        filer_models.load_backup_dir('dreambooths'),
        filer_models.load_backup_dir('loras'),
        filer_models.load_backup_dir('hypernetworks'),
        filer_models.load_backup_dir('extensions'),
        filer_models.load_backup_dir('images'),
        ]

elms = {}

def ui_dir(tab1):
    global elms

    if not tab1 in elms:
        elms[tab1] = {}

    with gr.Row():
        elms[tab1]['active_dir'] = gr.Textbox(value=globals()[f"FilerGroup{tab1}"].get_active_dir(), label="Active Dir", interactive=False)
        elms[tab1]['backup_dir'] = gr.Textbox(value=filer_models.load_backup_dir(tab1.lower()),label="Backup Dir", interactive=False)

def ui_set(tab1, tab2):
    global elms, out_html

    if not tab1 in elms:
        elms[tab1] = {}
    if not tab2 in elms[tab1]:
        elms[tab1][tab2] = {}

    if tab2 == 'Download':
        elms[tab1][tab2]['urls'] = gr.Textbox(
            label='URL per line',
            lines=10,
            interactive=True
        )
        elms[tab1][tab2]['download'] = gr.Button("Download to Active Dir")
        elms[tab1][tab2]['download'].click(
            fn=globals()[f"FilerGroup{tab1}"].download_urls,
            inputs=[elms[tab1][tab2]['urls']],
#            outputs=[elms[tab1][tab2]['table']],
            outputs=[out_html],
        )
        return

    with gr.Row():
        elms[tab1][tab2]['reload'] = gr.Button("Reload")
        elms[tab1][tab2]['select_all'] = gr.Button("Select All")
        elms[tab1][tab2]['deselect_all'] = gr.Button("Deselect All")
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
        elms[tab1][tab2]['table'] = gr.HTML("Please push Reload button.")
    with gr.Row():
        elms[tab1][tab2]['files'] = gr.Files(interactive=True)

    elms[tab1][tab2]['download'].click(
        fn=getattr(globals()[f"FilerGroup{tab1}"], f"download_{tab2.lower()}"),
        _js="function(){return rows('"+tab1.lower()+"_"+tab2.lower()+"')}",
        inputs=[elms[tab1][tab2]['selected']],
        outputs=[elms[tab1][tab2]['files']],
    )

    elms[tab1][tab2]['files'].upload(
        fn=getattr(globals()[f"FilerGroup{tab1}"], f"upload_{tab2.lower()}"),
        inputs=[elms[tab1][tab2]['files']],
        outputs=[elms[tab1][tab2]['table']],
    )

    if tab1 in ['Checkpoints', 'Hypernetworks'] and tab2 == 'Active':
        elms[tab1][tab2]['reload'].click(
            fn=getattr(globals()[f"FilerGroup{tab1}"], f"reload_{tab2.lower()}"),
            _js=f"reload_{tab1.lower()}",
            inputs=[],
            outputs=[elms[tab1][tab2]['table']],
        )
    else:
        elms[tab1][tab2]['reload'].click(
            fn=getattr(globals()[f"FilerGroup{tab1}"], f"reload_{tab2.lower()}"),
            inputs=[],
            outputs=[elms[tab1][tab2]['table'], elms[tab1][tab2]['selected']],
        )

    if tab1 == 'Checkpoints':
        elms[tab1][tab2]['invokeai'].click(
            fn=getattr(globals()[f"FilerGroup{tab1}"], f"make_{tab2.lower()}"),
            _js="function(){return rows('"+tab1.lower()+"_"+tab2.lower()+"')}",
            inputs=[elms[tab1][tab2]['selected']],
            outputs=[elms[tab1][tab2]['table']],
        )
        elms[tab1][tab2]['safetensors'].click(
            fn=getattr(globals()[f"FilerGroup{tab1}"], f"convert_{tab2.lower()}"),
            _js="function(){return rows('"+tab1.lower()+"_"+tab2.lower()+"')}",
            inputs=[elms[tab1][tab2]['selected']],
            outputs=[elms[tab1][tab2]['table']],
        )

    if tab1 in ['Checkpoints', 'Hypernetworks', 'Loras']:
        elms[tab1][tab2]['calc_sha256'].click(
            fn=getattr(globals()[f"FilerGroup{tab1}"], f"calc_{tab2.lower()}"),
            _js="function(){return rows('"+tab1.lower()+"_"+tab2.lower()+"')}",
            inputs=[elms[tab1][tab2]['selected']],
            outputs=[elms[tab1][tab2]['table']],
        )

    if tab1 == 'Hypernetworks':
        elms[tab1][tab2]['title'] = gr.Text(elem_id=f"{tab1.lower()}_{tab2.lower()}_title", visible=False).style(container=False)
        elms[tab1][tab2]['state'] = gr.Button(elem_id=f"state_{tab1.lower()}_{tab2.lower()}_button", visible=False).style(container=False)
        elms[tab1][tab2]['state'].click(
            fn=getattr(globals()[f"FilerGroup{tab1}"], f"state_{tab2.lower()}"),
            inputs=[elms[tab1][tab2]['title']],
            outputs=[out_html],
        )

    elms[tab1][tab2]['copy'].click(
        fn=getattr(globals()[f"FilerGroup{tab1}"], f"copy_{tab2.lower()}"),
        _js="function(){return rows('"+tab1.lower()+"_"+tab2.lower()+"')}",
        inputs=[elms[tab1][tab2]['selected']],
        outputs=[elms[tab1][tab2]['table']],
    )

    elms[tab1][tab2]['move'].click(
        fn=getattr(globals()[f"FilerGroup{tab1}"], f"move_{tab2.lower()}"),
        _js="function(){return rows('"+tab1.lower()+"_"+tab2.lower()+"')}",
        inputs=[elms[tab1][tab2]['selected']],
        outputs=[elms[tab1][tab2]['table']],
    )

    elms[tab1][tab2]['delete'].click(
        fn=getattr(globals()[f"FilerGroup{tab1}"], f"delete_{tab2.lower()}"),
        _js="function(){return rows('"+tab1.lower()+"_"+tab2.lower()+"')}",
        inputs=[elms[tab1][tab2]['selected']],
        outputs=[elms[tab1][tab2]['table']],
    )

    elms[tab1][tab2]['select_all'].click(fn=js_only,_js="function(){return select_all('"+tab1.lower()+"_"+tab2.lower()+"', true)}")
    elms[tab1][tab2]['deselect_all'].click(fn=js_only,_js="function(){return select_all('"+tab1.lower()+"_"+tab2.lower()+"', false)}")

out_html = None
def on_ui_tabs():
    global out_html
    with gr.Blocks() as filer:
        with gr.Row(equal_height=True):
            out_html = gr.HTML(check_backup_dir())
        with gr.Tabs() as tabs:
            with gr.TabItem("Checkpoints"):
                ui_dir("Checkpoints")
                with gr.Tabs() as tabs:
                    with gr.TabItem("Active"):
                        ui_set("Checkpoints", "Active")
                    with gr.TabItem("Backup"):
                        ui_set("Checkpoints", "Backup")
                    with gr.TabItem("Download"):
                        ui_set("Checkpoints", "Download")
            with gr.TabItem("Embeddings"):
                ui_dir("Embeddings")
                with gr.Tabs() as tabs:
                    with gr.TabItem("Active"):
                        ui_set("Embeddings", "Active")
                    with gr.TabItem("Backup"):
                        ui_set("Embeddings", "Backup")
                    with gr.TabItem("Download"):
                        ui_set("Embeddings", "Download")
            with gr.TabItem("Dreambooths"):
                ui_dir("Dreambooths")
                with gr.Tabs() as tabs:
                    with gr.TabItem("Active"):
                        ui_set("Dreambooths", "Active")
                    with gr.TabItem("Backup"):
                        ui_set("Dreambooths", "Backup")
            with gr.TabItem("Loras"):
                ui_dir("Loras")
                with gr.Tabs() as tabs:
                    with gr.TabItem("Active"):
                        ui_set("Loras", "Active")
                    with gr.TabItem("Backup"):
                        ui_set("Loras", "Backup")
                    with gr.TabItem("Download"):
                        ui_set("Loras", "Download")
            with gr.TabItem("Hypernetworks"):
                ui_dir("Hypernetworks")
                with gr.Tabs() as tabs:
                    with gr.TabItem("Active"):
                        ui_set("Hypernetworks", "Active")
                    with gr.TabItem("Backup"):
                        ui_set("Hypernetworks", "Backup")
                    with gr.TabItem("Download"):
                        ui_set("Hypernetworks", "Download")
            with gr.TabItem("Extensions"):
                ui_dir("Extensions")
                with gr.Tabs() as tabs:
                    with gr.TabItem("Active"):
                        ui_set("Extensions", "Active")
                    with gr.TabItem("Backup"):
                        ui_set("Extensions", "Backup")
            with gr.TabItem("Images"):
                ui_dir("Images")
                with gr.Tabs() as tabs:
                    with gr.TabItem("Active"):
                        ui_set("Images", "Active")
                    with gr.TabItem("Backup"):
                        ui_set("Images", "Backup")
            with gr.TabItem("Files"):
                files_reload = gr.Button("Reload")
                files_table = gr.HTML("Please push Reload button.")
                files_title = gr.Text(elem_id=f"files_title", visible=False).style(container=False)
                files_load = gr.Button(elem_id=f"load_files_button", visible=False).style(container=False)
                files_download = gr.Button(elem_id=f"download_files_button", visible=False).style(container=False)
                files_edit = gr.Textbox(lines=10,interactive=True,label='Loaded File')
                files_save = gr.Button("Save")
                files_files = gr.Files(interactive=False)
                files_reload.click(
                    fn=FilerGroupFiles._table,
                    inputs=[],
                    outputs=[files_table],
                    )
                files_load.click(
                    fn=FilerGroupFiles.load,
                    inputs=[files_title],
                    outputs=[files_edit],
                    )
                files_save.click(
                    fn=FilerGroupFiles.save,
                    inputs=[files_title, files_edit],
                    outputs=[out_html],
                    )
                files_download.click(
                    fn=FilerGroupFiles.download,
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
            outputs=[
                out_html,
                elms['Checkpoints']['backup_dir'],
                elms['Dreambooths']['backup_dir'],
                elms['Loras']['backup_dir'],
                elms['Hypernetworks']['backup_dir'],
                elms['Extensions']['backup_dir'],
                elms['Images']['backup_dir'],
                ])

    return (filer, "Filer", "filer"),


script_callbacks.on_ui_tabs(on_ui_tabs)
