'use strinct'


// add button function
const addBtn = document.getElementById('addBtn')

addBtn.onclick = () => {
    const teacher_id = document.getElementById('add_teacher_id').value
    const group_id = document.getElementById('add_group_id').value
    const subject_id = document.getElementById('add_subject_id').value

    const data = {
        teacher_id: teacher_id,
        group_id: group_id,
        subject_id: subject_id,
    }

    fetch('http://127.0.0.1:8000/', {
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

// delete button

function deleteData(item_id) {
    const data = {
        item_id: item_id
    }

    fetch('http://127.0.0.1:8000/', {
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
        alert('Запись удалена из базы данных')
        window.location.reload()
    }).catch(error => {
        alert('Ошибка при удалении из базы данных', error)
    })
}


// editData 
const teacher_id = document.getElementById('edit_teacher_id')
const group_id = document.getElementById('edit_group_id')
const subject_id = document.getElementById('edit_subject_id')
let data_id = null

function editData(data) {
    teacher_id.value = data.teacher_id
    group_id.value = data.group_id
    subject_id.value = data.subject_id
    data_id = data.id
}


// save changes data
function saveData() {
    const data = {
        teacher_id: teacher_id.value,
        group_id: group_id.value,
        subject_id: subject_id.value,
        data_id: data_id,
    }

    fetch('http://127.0.0.1:8000/', {
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
        alert('Данные успено сохранены в БД')
        window.location.reload()
    }).catch(error => {
        alert('Ошибка при сохранении данных в БД,', error)
    })
}