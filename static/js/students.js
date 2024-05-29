'use strict'


const student_add_btn = document.getElementById('student_add_btn')


student_add_btn.onclick = () => {
    const data = {
        first_name: document.getElementById('first_name_input').value,
        last_name: document.getElementById('last_name_input').value,
        group_id: document.getElementById('group_id_select').value
    }

    fetch('http://127.0.0.1:5000/students', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json()
    }).then(data => {
        alert('Данные успено сохранены в БД,')
        window.location.reload()
    }).catch(error => {
        alert('Ошибка при добавлении в БД,', error)
    })
}