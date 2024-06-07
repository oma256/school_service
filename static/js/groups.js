'use strict'


// Логика добавления группы в Базу Данных
const group_add_btn = document.getElementById('group_add_btn')

group_add_btn.onclick = () => {
    const data = {
        group_name: document.getElementById('group_name_input').value
    }

    fetch('http://127.0.0.1:8000/groups', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    }).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json()
    }).then(data => {
        if (data.status == 'FAILED') {
            alert('Такая группа уже существует в БД')
        } else {
            alert('Данные успено сохранены в БД')
            window.location.reload()
        }
    }).catch(error => {
        console.log('Ошибка при добавлении в БД,', error)
    })
}


// Логика удаления группы из базы данных

const groupDeleteButtons = document.getElementsByClassName('btn-danger')

for (let button of groupDeleteButtons) {
    button.addEventListener('click', function (event) {
        const listItem = event.target.parentElement;
        listItem.remove();
    });
}
