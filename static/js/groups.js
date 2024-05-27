'use strict'

const data = {
    name: 'Название группу'
}

const group_add_btn = document.getElementById('group_add_btn')

group_add_btn.onclick = () => {
    fetch('http://localhost:5000/groups', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(data),
    }).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json()
    }).then(data => {
        console.log('Данные успено сохранены в БД,', data)
    }).catch(error => {
        console.log('Ошибка при добавлении в БД,', error)
    })
}


const getCookie = (name) => {
    return document.cookie.split(';').reduce((prev, c) => {
        let arr = c.split('=');
        return (arr[0].trim() === name) ? arr[1] : prev;
    }, undefined);
};
