
function reload_checkpoints(_, _){
    gradioApp().querySelector('#refresh_sd_model_checkpoint').click()
}

function reload_hypernetworks(_, _){
    gradioApp().querySelector('#refresh_sd_hypernetwork').click()
}

function state(button, name, title) {
    textarea = gradioApp().querySelector('#'+name+'_title textarea')
    textarea.value = title
	textarea.dispatchEvent(new Event("input", { bubbles: true }))
    gradioApp().querySelector('#state_'+name+'_button').click()
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
