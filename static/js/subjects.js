'use strict'

const subject_btn = document.getElementById('subject_add_btn')

subject_btn.onclick = () => {
    const data = {
        subject_name: document.getElementById('subject_name_input').value
    }

    fetch('http://127.0.0.1:5000/subjects', {
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