function save_checkpoints(name){
    list = {}
    gradioApp().querySelectorAll('.filer_'+name+'_row').forEach(function(row){
		idx = row.querySelector('td .filer_genre').selectedIndex
        list[row.dataset.title] = {
            "genre": row.querySelector('td .filer_genre').options[idx].value,
            "comment": row.querySelector('td .filer_comment').value
        }
    })

    return JSON.stringify(list)
}

function save_hypernetworks(name){
    list = {}
    gradioApp().querySelectorAll('.filer_'+name+'_row').forEach(function(row){
        list[row.dataset.title] = {
            "model": row.querySelector('td .filer_model').value,
            "comment": row.querySelector('td .filer_comment').value
        }
    })

    return JSON.stringify(list)
}

function save_extensions(name){
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
	return save_checkpoints('checkpoints_active')
}

function save_checkpoints_backup(_, _){
	return save_checkpoints('checkpoints_backup')
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
	return save_hypernetworks('hypernetworks_active')
}

function save_hypernetworks_backup(_, _){
	return save_hypernetworks('hypernetworks_backup')
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
	return save_extensions('extensions_active')
}

function save_extensions_backup(_, _){
	return save_extensions('extensions_backup')
}
// paste end
