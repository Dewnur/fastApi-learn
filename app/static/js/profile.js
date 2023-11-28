const field_values = []

function hide_edit_btn() {
    hide("btn-edit-profile")
    hide("btn-save")
    hide("btn-cancel")
}

function hide(id) {
    const toBeHidden = document.getElementById(id);
    if (toBeHidden.style.display === "none") {
        toBeHidden.style.display = "block";
    } else {
        toBeHidden.style.display = "none";
    }
}

function open_edit_profile() {
    hide_edit_btn()
    const input_fields = document.getElementsByName("profile-input")
    input_fields.forEach((element) => field_values.push(element.value))
    input_fields.forEach((element) => element.className = "form-control")
}

function cancel_edit() {
    hide_edit_btn()
    const input_fields = document.getElementsByName("profile-input")
    input_fields.forEach((element) => element.className = "form-control-plaintext")
    for (let i = 0; i < input_fields.length; i++) {
        input_fields[i].value = field_values[i]
    }
}