'use strict'

function addTeacher() {
    const firstName = document.getElementById('first_name_input').value
    const lastName = document.getElementById('last_name_input').value
    const positionId = document.getElementById('add_position_id').value

    const data = {
        first_name: firstName,
        last_name: lastName,
        position_id: positionId,
    }

    fetch('http://127.0.0.1:8000/teachers', {
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
        alert('Преподаватель успешно добавлен в базу данных')
        window.location.reload()
    }).catch(error => {
        alert('Ошибка при добавлении в базу данных', error)
    })
}


function deleteTeacher(teacherId) {
    const data = {
        teacher_id: teacherId
    }

    fetch('http://127.0.0.1:8000/teachers', {
        method: 'DELETE',
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
        alert('Преподаватель удален из базы данных')
        window.location.reload()
    }).catch(error => {
        alert('Ошибка при удалении из базы данных', error)
    })
}

const edit_first_name = document.getElementById('edit_first_name')
const edit_last_name = document.getElementById('edit_last_name')
const edit_position_id = document.getElementById('edit_position_id')
let teacherId = null


function editTeacher(teacher) {
    edit_first_name.value = teacher.first_name
    edit_last_name.value = teacher.last_name
    edit_position_id.value = teacher.position_id
    teacherId = teacher.id
}

function saveTeacherData() {
    const firstName = document.getElementById('edit_first_name').value
    const lastName = document.getElementById('edit_last_name').value
    const positionId = document.getElementById('edit_position_id').value

    const data = {
        first_name: firstName,
        last_name: lastName,
        position_id: positionId,
        teacher_id: teacherId,
    }

    fetch('http://127.0.0.1:8000/teachers', {
        method: 'PUT',
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
        alert('Данные успешно обновлены')
        window.location.reload()
    }).catch(error => {
        alert('Ошибка сохранении в базе данных', error)
    })
}