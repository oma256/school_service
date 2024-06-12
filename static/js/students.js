'use strict'

// button for edit student data to database

const edit_first_name = document.getElementById('edit_first_name')
const edit_last_name = document.getElementById('edit_last_name')
const edit_group_id = document.getElementById('edit_group_id')
let student_id = null


function editStudent(student) {
    edit_first_name.value = student.first_name
    edit_last_name.value = student.last_name
    edit_group_id.value = student.group_id
    student_id = student.id
}


function saveStudentData() {
    const data = {
        first_name: edit_first_name.value,
        last_name: edit_last_name.value,
        group_id: edit_group_id.value,
        student_id: student_id,
    }

    fetch('http://127.0.0.1:8000/students', {
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
        alert('Данные успено сохранены в БД,')
        window.location.reload()
    }).catch(error => {
        alert('Ошибка при сохранении данных в БД,', error)
    })
}


// button for delete student from database


function deleteStudent(student_id) {
    const data = {
        student_id: student_id
    }

    fetch('http://127.0.0.1:8000/students', {
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
        alert('Студент удале из базы данных')
        window.location.reload()
    }).catch(error => {
        alert('Ошибка при удалении из базы данных', error)
    })
    
}


function addStudent() {
    const firstName = document.getElementById('first_name_input').value
    const lastName = document.getElementById('last_name_input').value
    const groupId = document.getElementById('add_group_id').value

    const data = {
        first_name: firstName,
        last_name: lastName,
        group_id: groupId,
    }

    fetch('http://127.0.0.1:8000/students', {
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
        alert('Студент успешно добавлен базу данных')
        window.location.reload()
    }).catch(error => {
        alert('Ошибка при добавлении в базу данных', error)
    })
}