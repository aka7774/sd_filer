function save_checkpoints(_, _){
    list = {}
    gradioApp().querySelectorAll('.filer_checkpoints_active_row').forEach(function(row){
		idx = row.querySelector('td .filer_genre').selectedIndex
        list[row.dataset.title] = {
            "genre": row.querySelector('td .filer_genre').options[idx].value,
            "comment": row.querySelector('td .filer_comment').value
        }
    })

    return JSON.stringify(list)
}

function rows_checkpoints_active(_, _){
	return rows('checkpoints_active')
}

function rows_checkpoints_backup(_, _){
	return rows('checkpoints_backup')
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

function reload_checkpoints(_, _){
    gradioApp().querySelector('#refresh_sd_model_checkpoint').click()
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

function select_all(name, che){
    gradioApp().querySelectorAll('.filer_'+name+'_select').forEach(function(x){
        x.checked = che
    })
	rows(name)
}
