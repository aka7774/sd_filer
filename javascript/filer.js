function save_comments(name){
    list = {}
    gradioApp().querySelectorAll('.filer_'+name+'_row').forEach(function(row){
        list[row.dataset.title] = {
            "comment": row.querySelector('td .filer_comment').value
        }
    })

    return JSON.stringify(list)
}

function reload_checkpoints(_, _){
    gradioApp().querySelector('#refresh_sd_model_checkpoint').click()
}

function reload_hypernetworks(_, _){
    gradioApp().querySelector('#refresh_sd_hypernetwork').click()
}

function state_hypernetworks(name, title) {
    textarea = gradioApp().querySelector('#'+name+'_title textarea')
    textarea.value = title
	textarea.dispatchEvent(new Event("input", { bubbles: true }))
    gradioApp().querySelector('#state_'+name+'_button').click()
}

function state_hypernetworks_active(button, title){
	return state_hypernetworks('hypernetworks_active', title)
}

function state_hypernetworks_backup(button, title){
	return state_hypernetworks('hypernetworks_backup', title)
}

function load_files(button, title) {
	name = 'files'
    textarea = gradioApp().querySelector('#'+name+'_title textarea')
    textarea.value = title
	textarea.dispatchEvent(new Event("input", { bubbles: true }))
    gradioApp().querySelector('#load_'+name+'_button').click()
}

function download_files(button, title) {
	name = 'files'
    textarea = gradioApp().querySelector('#'+name+'_title textarea')
    textarea.value = title
	textarea.dispatchEvent(new Event("input", { bubbles: true }))
    gradioApp().querySelector('#download_'+name+'_button').click()
}

function rows(name){
    selected = []
    gradioApp().querySelectorAll('.filer_'+name+'_select').forEach(function(x){
        if(x.checked){
            selected.push(x.closest('.filer_'+name+'_row').dataset.title)
        }
    })

    gradioApp().querySelector('#filer_'+name+'_selected label textarea').value = selected.join(",");
 	return selected.join(",")
}

function select_all(name, che){
    gradioApp().querySelectorAll('.filer_'+name+'_select').forEach(function(x){
        x.checked = che
    })
	rows(name)
}

// copy begin
function rows_checkpoints_active(_, _){
	return rows('checkpoints_active')
}

function rows_checkpoints_backup(_, _){
	return rows('checkpoints_backup')
}

function select_all_checkpoints_active(_, _){
	select_all('checkpoints_active', true)
}

function select_all_checkpoints_backup(_, _){
	select_all('checkpoints_backup', true)
}

function deselect_all_checkpoints_active(_, _){
	select_all('checkpoints_active', false)
}

function deselect_all_checkpoints_backup(_, _){
	select_all('checkpoints_backup', false)
}

function save_checkpoints_active(_, _){
	return save_comments('checkpoints_active')
}

function save_checkpoints_backup(_, _){
	return save_comments('checkpoints_backup')
}
// copy end

// paste begin
function rows_hypernetworks_active(_, _){
	return rows('hypernetworks_active')
}

function rows_hypernetworks_backup(_, _){
	return rows('hypernetworks_backup')
}

function select_all_hypernetworks_active(_, _){
	select_all('hypernetworks_active', true)
}

function select_all_hypernetworks_backup(_, _){
	select_all('hypernetworks_backup', true)
}

function deselect_all_hypernetworks_active(_, _){
	select_all('hypernetworks_active', false)
}

function deselect_all_hypernetworks_backup(_, _){
	select_all('hypernetworks_backup', false)
}

function save_hypernetworks_active(_, _){
	return save_comments('hypernetworks_active')
}

function save_hypernetworks_backup(_, _){
	return save_comments('hypernetworks_backup')
}
//
function rows_extensions_active(_, _){
	return rows('extensions_active')
}

function rows_extensions_backup(_, _){
	return rows('extensions_backup')
}

function select_all_extensions_active(_, _){
	select_all('extensions_active', true)
}

function select_all_extensions_backup(_, _){
	select_all('extensions_backup', true)
}

function deselect_all_extensions_active(_, _){
	select_all('extensions_active', false)
}

function deselect_all_extensions_backup(_, _){
	select_all('extensions_backup', false)
}

function save_extensions_active(_, _){
	return save_comments('extensions_active')
}

function save_extensions_backup(_, _){
	return save_comments('extensions_backup')
}
//
function rows_images_active(_, _){
	return rows('images_active')
}

function rows_images_backup(_, _){
	return rows('images_backup')
}

function select_all_images_active(_, _){
	select_all('images_active', true)
}

function select_all_images_backup(_, _){
	select_all('images_backup', true)
}

function deselect_all_images_active(_, _){
	select_all('images_active', false)
}

function deselect_all_images_backup(_, _){
	select_all('images_backup', false)
}

function save_images_active(_, _){
	return save_comments('images_active')
}

function save_images_backup(_, _){
	return save_comments('images_backup')
}
//
function rows_dreambooths_active(_, _){
	return rows('dreambooths_active')
}

function rows_dreambooths_backup(_, _){
	return rows('dreambooths_backup')
}

function select_all_dreambooths_active(_, _){
	select_all('dreambooths_active', true)
}

function select_all_dreambooths_backup(_, _){
	select_all('dreambooths_backup', true)
}

function deselect_all_dreambooths_active(_, _){
	select_all('dreambooths_active', false)
}

function deselect_all_dreambooths_backup(_, _){
	select_all('dreambooths_backup', false)
}

function save_dreambooths_active(_, _){
	return save_comments('dreambooths_active')
}

function save_dreambooths_backup(_, _){
	return save_comments('dreambooths_backup')
}
//
function rows_loras_active(_, _){
	return rows('loras_active')
}

function rows_loras_backup(_, _){
	return rows('loras_backup')
}

function select_all_loras_active(_, _){
	select_all('loras_active', true)
}

function select_all_loras_backup(_, _){
	select_all('loras_backup', true)
}

function deselect_all_loras_active(_, _){
	select_all('loras_active', false)
}

function deselect_all_loras_backup(_, _){
	select_all('loras_backup', false)
}

function save_loras_active(_, _){
	return save_comments('loras_active')
}

function save_loras_backup(_, _){
	return save_comments('loras_backup')
}
// paste end
