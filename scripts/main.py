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

def js_only():
    pass

# copy begin
def copy_checkpoints_active(filenames):
    filer_actions.copy(filenames, filer_checkpoints.list_active(), filer_models.load_backup_dir())
    return table_checkpoints_active()

def copy_checkpoints_backup(filenames):
    filer_actions.copy(filenames, filer_checkpoints.list_backup(), filer_checkpoints.load_active_dir())
    return table_checkpoints_backup()

def move_checkpoints_active(filenames):
    filer_actions.move(filenames, filer_checkpoints.list_active(), filer_models.load_backup_dir())
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

def table_checkpoints_active():
    return table_checkpoints('checkpoints_active', filer_checkpoints.list_active())

def table_checkpoints_backup():
    return table_checkpoints('checkpoints_backup', filer_checkpoints.list_backup())
# copy end

# paste
def copy_hypernetworks_active(filenames):
    filer_actions.copy(filenames, filer_hypernetworks.list_active(), filer_models.load_backup_dir())
    return table_hypernetworks_active()

def copy_hypernetworks_backup(filenames):
    filer_actions.copy(filenames, filer_hypernetworks.list_backup(), filer_hypernetworks.load_active_dir())
    return table_hypernetworks_backup()

def move_hypernetworks_active(filenames):
    filer_actions.move(filenames, filer_hypernetworks.list_active(), filer_models.load_backup_dir())
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
    return table_hypernetworks('hypernetworks_active', filer_hypernetworks.list_active())

def table_hypernetworks_backup():
    return table_hypernetworks('hypernetworks_backup', filer_hypernetworks.list_backup())
#
def copy_extensions_active(filenames):
    filer_actions.copy(filenames, filer_extensions.list_active(), filer_models.load_backup_dir())
    return table_extensions_active()

def copy_extensions_backup(filenames):
    filer_actions.copy(filenames, filer_extensions.list_backup(), filer_extensions.load_active_dir())
    return table_extensions_backup()

def move_extensions_active(filenames):
    filer_actions.move(filenames, filer_extensions.list_active(), filer_models.load_backup_dir())
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
    return table_extensions('extensions_active', filer_extensions.list_active())

def table_extensions_backup():
    return table_extensions('extensions_backup', filer_extensions.list_backup())
#
def copy_images_active(filenames):
    filer_actions.copy(filenames, filer_images.list_active(), filer_models.load_backup_dir())
    return table_images_active()

def copy_images_backup(filenames):
    filer_actions.copy(filenames, filer_images.list_backup(), filer_images.load_active_dir())
    return table_images_backup()

def move_images_active(filenames):
    filer_actions.move(filenames, filer_images.list_active(), filer_models.load_backup_dir())
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
    return table_images('images_active', filer_images.list_active())

def table_images_backup():
    return table_images('images_backup', filer_images.list_backup())
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

def save_backup_dir(backup_dir):
    filer_models.save_backup_dir(backup_dir)

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
        if tab1 in ['Checkpoints', 'Hypernetworks']:
            elms[tab1][tab2]['calc_sha256'] = gr.Button("Calc SHA256")
        elms[tab1][tab2]['copy'] = gr.Button("Copy")
        elms[tab1][tab2]['move'] = gr.Button("Move")
        elms[tab1][tab2]['delete'] = gr.Button("Delete")
    with gr.Row():
        elms[tab1][tab2]['table'] = gr.HTML()

    elms[tab1][tab2]['save'].click(
        fn=globals()[f"save_{tab1.lower()}"],
        _js=f"save_{tab1.lower()}_{tab2.lower()}",
        inputs=[elms[tab1][tab2]['selected']],
        outputs=[out_html],
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

    if tab1 in ['Checkpoints', 'Hypernetworks']:
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
    backup_dir_value = filer_models.load_backup_dir()
    with gr.Blocks() as filer:
        with gr.Row(equal_height=True):
            backup_dir = gr.Textbox(label="Backup Directory",value=backup_dir_value)
            out_html = gr.HTML()
        with gr.Tabs() as tabs:
            with gr.TabItem("Checkpoints"):
                with gr.Tabs() as tabs:
                    with gr.TabItem("Active"):
                        ui_set("Checkpoints", "Active")
                    with gr.TabItem("Backup"):
                        ui_set("Checkpoints", "Backup")
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
                    
        backup_dir.blur(
            fn=save_backup_dir,
            inputs=[backup_dir],
            outputs=[],
        )

    return (filer, "Filer", "filer"),


script_callbacks.on_ui_tabs(on_ui_tabs)

def table_checkpoints(name, rs):
    code = f"""
    <table>
        <thead>
            <tr>
                <th></th>
                <th>Filename</th>
                <th>hash</th>
                <th>sha256</th>
                <th>vae.pt</th>
                <th>yaml</th>
                <th>Genre</th>
                <th>Comment</th>
            </tr>
        </thead>
        <tbody>
    """

    for r in rs:
        op_html = ''
        for op in ['Default', 'Merged', 'Dreambooth', 'DreamArtist']:
            if op == r['genre']:
                op_html += '<option selected>' + op
            else:
                op_html += '<option>' + op

        code += f"""
            <tr class="filer_{name}_row" data-title="{r['title']}">
                <td class="filer_checkbox"><input class="filer_{name}_select" type="checkbox" onClick="rows_{name}()"></td>
                <td class="filer_filename">{r['filename']}</td>
                <td class="filer_hash">{r['hash']}</td>
                <td class="filer_sha256">{r['sha256']}</td>
                <td class="filer_vae">{r['vae']}</td>
                <td class="filer_yaml">{r['yaml']}</td>
                <td><select class="filer_genre">{op_html}</select></td>
                <td><input class="filer_comment" type="text" value="{r['comment']}"></td>
            </tr>
            """

    code += """
        </tbody>
    </table>
    """

    return code

def table_hypernetworks(name, rs):
    code = f"""
    <table>
        <thead>
            <tr>
                <th></th>
                <th>Filename</th>
                <th>state</th>
                <th>hash</th>
                <th>sha256</th>
                <th>Model</th>
                <th>Comment</th>
            </tr>
        </thead>
        <tbody>
    """

    for r in rs:
        code += f"""
            <tr class="filer_{name}_row" data-title="{r['title']}">
                <td class="filer_checkbox"><input class="filer_{name}_select" type="checkbox" onClick="rows_{name}()"></td>
                <td class="filer_filename">{r['filename']}</td>
                <td class="filer_state"><input onclick="state_{name}(this, '{r['title']}')" type="button" value="state" class="gr-button gr-button-lg gr-button-secondary"></td>
                <td class="filer_hash">{r['hash']}</td>
                <td class="filer_sha256">{r['sha256']}</td>
                <td><input class="filer_model" type="text" value="{r['model']}"></td>
                <td><input class="filer_comment" type="text" value="{r['comment']}"></td>
            </tr>
            """

    code += """
        </tbody>
    </table>
    """

    return code

def table_extensions(name, rs):
    code = f"""
    <table>
        <thead>
            <tr>
                <th></th>
                <th>name</th>
                <th>Comment</th>
            </tr>
        </thead>
        <tbody>
    """

    for r in rs:
        code += f"""
            <tr class="filer_{name}_row" data-title="{r['title']}">
                <td class="filer_checkbox"><input class="filer_{name}_select" type="checkbox" onClick="rows_{name}()"></td>
                <td class="filer_filename">{r['filename']}</td>
                <td><input class="filer_comment" type="text" value="{r['comment']}"></td>
            </tr>
            """

    code += """
        </tbody>
    </table>
    """

    return code

def table_images(name, rs):
    code = f"""
    <table>
        <thead>
            <tr>
                <th></th>
                <th>name</th>
                <th>path</th>
                <th>files</th>
                <th>Comment</th>
            </tr>
        </thead>
        <tbody>
    """

    for r in rs:
        code += f"""
            <tr class="filer_{name}_row" data-title="{r['title']}">
                <td class="filer_checkbox"><input class="filer_{name}_select" type="checkbox" onClick="rows_{name}()"></td>
                <td class="filer_filename">{r['filename']}</td>
                <td class="filer_filepath">{r['filepath']}</td>
                <td class="filer_files">{r['files']}</td>
                <td><input class="filer_comment" type="text" value="{r['comment']}"></td>
            </tr>
            """

    code += """
        </tbody>
    </table>
    """

    return code