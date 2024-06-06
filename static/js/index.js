'use strinct'

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