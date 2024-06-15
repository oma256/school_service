'use strict'

function addData() {
    const data = {
        subject_name: document.getElementById('subject_name_input').value
    }

    fetch('http://127.0.0.1:8000/subjects', {
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
        alert('Предмет добавлен в БД')
        window.location.reload()
    }).catch(error => {
        alert('Ошибка при добавлении в БД', error)
    })
}

function deleteSubject(subjectId) {
    const data = {subject_id: subjectId}

    fetch('http://127.0.0.1:8000/subjects', {
        method: 'DELETE',
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
        alert('Предмет удален из БД')
        window.location.reload()
    }).catch(error => {
        alert('Ошибка при удалении', error)
    })
}

const edit_subject_input = document.getElementById('edit_subject_name')
let subject_id = null

function editSubject(subject) {
    edit_subject_input.value = subject.name
    subject_id = subject.id 
}

function saveSubjectData() {
    const data = {
        subject_name: edit_subject_input.value,
        subject_id: subject_id,
    }

    fetch('http://127.0.0.1:8000/subjects', {
        method: 'PUT',
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
        alert('Данные успешео обновлены в БД')
        window.location.reload()
    }).catch(error => {
        alert('Ошибка обновлении', error)
    })
}