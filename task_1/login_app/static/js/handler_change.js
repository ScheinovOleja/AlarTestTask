const save_link = document.getElementById('save_user')
const csrfToken = $("input[name='csrfmiddlewaretoken']").val();


function save_user(e) {
    e.preventDefault()
    let id = e.currentTarget.dataset.id
    let username = $("input[name='username']").val();
    let email = $("input[name='email']").val();
    let cur_pass = $("input[name='cur_pass']").val();
    let pass1 = $("input[name='pass1']").val();
    let pass2 = $("input[name='pass2']").val();
    let select = document.getElementById("role");
    let value = select.options[select.selectedIndex].value;
    let data = {
        'username': username,
        'email': email,
        'cur_pass': cur_pass,
        'pass1': pass1,
        'pass2': pass2,
        'id': id,
        'role': value
    }
    $.ajax({
        type: "POST",
        headers: {'X-CSRFToken': csrfToken},
        mode: 'same-origin',
        dataType: 'json',
        contentType: 'application/json',
        url: "/change_user",
        data: JSON.stringify(data),
        success: function (response) {
            $("input[name='cur_pass']").val('');
            $("input[name='pass1']").val('');
            $("input[name='pass2']").val('');
            alert(response['msg']);
        }
    });
    return true;
}


save_link.addEventListener('click', save_user)

