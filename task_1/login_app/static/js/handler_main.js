const delete_link = document.getElementsByName('delete')
const add_link = document.getElementById('add_user')
const csrfToken = $("input[name='csrfmiddlewaretoken']").val();


function add_user(e) {
    e.preventDefault()
    alert('Удалить')
}


function delete_user(e) {
    e.preventDefault()
    let data = {
        'id': e.currentTarget.dataset.id,
    }
    $.ajax({
        type: "POST",
        headers: {'X-CSRFToken': csrfToken},
        mode: 'same-origin',
        dataType: 'json',
        contentType: 'application/json',
        url: "/delete_user",
        data: JSON.stringify(data),
        success: function (response) {
            alert(response['msg']);
            location.reload()
        }
    });
    return true;
}

for (let link of delete_link){
    link.addEventListener('click', delete_user)
}

add_link.addEventListener('click', add_user)