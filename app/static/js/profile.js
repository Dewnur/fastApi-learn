const field_values = []

function toggleDisplay(element) {
    if (element.style.display === "none") {
        element.style.display = "block";
    } else {
        element.style.display = "none";
    }
}

function toggleReadonly(element) {
    if (element.hasAttribute("readonly")) {
        element.removeAttribute("readonly", "true");
    } else {
        element.setAttribute("readonly", "true");
    }
}

function hide_edit_btn() {
    const edit_btn_id_list = ["btn-edit-profile", "btn-save", "btn-cancel"]
    for (const id in edit_btn_id_list) {
        const element = document.getElementById(edit_btn_id_list[id])
        toggleDisplay(element)
    }
}

function open_edit_profile() {
    hide_edit_btn()
    const input_fields = document.getElementsByName("profile-input")
    input_fields.forEach((element) => field_values.push(element.value))
    input_fields.forEach((element) => element.className = "form-control")
    input_fields.forEach((element) => toggleReadonly(element))

}

function cancel_edit() {
    hide_edit_btn()
    const input_fields = document.getElementsByName("profile-input")
    input_fields.forEach((element) => element.className = "form-control-plaintext")
    input_fields.forEach((element) => toggleReadonly(element))

    for (let i = 0; i < input_fields.length; i++) {
        input_fields[i].value = field_values[i]
    }
}