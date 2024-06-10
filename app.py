from flask import Flask, render_template, g, request
from flask_cors import CORS
import psycopg2
from database import db_connect

from helpers import (
    get_group_list,
    get_students_list,
    get_subjects_list,
    get_teachers_list,
    get_index_page_data,
    get_positions_list,
)


app = Flask(__name__)
CORS(app=app)


@app.route('/', methods=['GET', 'POST', 'DELETE', 'PUT'])
@db_connect
def index():
    db_cursor = g.db_conn.cursor()
    
    if request.method == 'GET':
        data = get_index_page_data()
        return render_template(template_name_or_list='index.html', data=data)
    
    elif request.method == 'POST':
        teacher_id = int(request.json.get('teacher_id'))
        group_id = int(request.json.get('group_id'))
        subject_id = int(request.json.get('subject_id'))

        db_cursor.execute(
            'INSERT INTO t_teachers_groups_subjects (teacher_id, group_id, subject_id) VALUES (%s, %s, %s)',
            (teacher_id, group_id, subject_id)
        )

        return {'status': 'OK'}

    elif request.method == 'DELETE':
        item_id = int(request.json.get('item_id'))

        db_cursor.execute('DELETE FROM t_teachers_groups_subjects WHERE id=%s', 
                          (item_id,))

        return {'status': 'OK'}

    elif request.method == 'PUT':
        teacher_id = int(request.json.get('teacher_id'))
        group_id = int(request.json.get('group_id'))
        subject_id = int(request.json.get('subject_id'))
        data_id = int(request.json.get('data_id'))

        db_cursor.execute('UPDATE t_teachers_groups_subjects SET teacher_id=%s, group_id=%s, subject_id=%s WHERE id=%s',
                          (teacher_id, group_id, subject_id, data_id))

        return {'status': 'OK'}


@app.route('/students', methods=['GET', 'POST', 'PUT', 'DELETE'])
@db_connect
def students():
    db_cursor = g.db_conn.cursor()

    if request.method == 'GET':
        if request.args.get('group_id'):
            group_id = request.args.get('group_id')
            db_cursor.execute('SELECT * FROM t_student WHERE group_id=%s', 
                              (group_id,))
        else:
            db_cursor.execute('SELECT * FROM t_student')

        student_list = db_cursor.fetchall()
        students = get_students_list(students=student_list)

        db_cursor.execute('SELECT * FROM t_group')
        group_list = db_cursor.fetchall()
        groups = get_group_list(groups=group_list)

        return render_template('students.html', students=students, groups=groups)
    
    elif request.method == 'POST':
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        group_id = int(request.json.get('group_id'))

        db_cursor.execute(
            'INSERT INTO t_student (first_name, last_name, group_id) VALUES (%s, %s, %s)', 
            (first_name, last_name, group_id))

        return {'status': 'OK'}
    
    elif request.method == 'PUT':
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        group_id = int(request.json.get('group_id'))
        student_id = int(request.json.get('student_id'))

        db_cursor.execute('UPDATE t_student SET first_name=%s, last_name=%s, group_id=%s WHERE id=%s',
                          (first_name, last_name, group_id, student_id))

        return {'status': 'OK'}

    elif request.method == 'DELETE':
        student_id = request.json.get('student_id')
        try:
            db_cursor.execute('DELETE FROM t_student WHERE id=%s', (student_id,))
        except psycopg2.errors.ForeignKeyViolation as e:
            return {'status': 'FAILED'}
        return {'status': 'OK'}


@app.route('/groups', methods=['GET', 'POST', 'DELETE'])
@db_connect
def groups():
    db_cursor = g.db_conn.cursor()
    
    if request.method == 'GET':
        db_cursor.execute('SELECT * FROM t_group;')
        group_list = db_cursor.fetchall()
        groups = get_group_list(groups=group_list)

        return render_template('groups.html', groups=groups)
    elif request.method == 'POST':
        group_name = request.json.get('group_name')

        db_cursor.execute('SELECT * FROM t_group WHERE name=%s',
                          (group_name,))
        group = db_cursor.fetchone()

        if group:
            return {'status': 'FAILED'}
        else:
            db_cursor.execute('INSERT INTO t_group (name) VALUES (%s)', 
                            (group_name,))

            return {'status': 'OK'}
    elif request.method == 'DELETE':
        group_id = request.json.get('group_id')

        db_cursor.execute('DELETE FROM t_group WHERE id=%s', (group_id,))

        return {'status': 'OK'}


@app.route('/teachers', methods=['GET'])
@db_connect
def teachers():
    db_cursor = g.db_conn.cursor()
    db_cursor.execute('SELECT * FROM t_teacher;')
    teacher_list = db_cursor.fetchall()
    teachers = get_teachers_list(teachers=teacher_list)

    return render_template('teachers.html', teachers=teachers)


@app.route('/positions', methods=['GET', 'POST', 'PUT', 'DELETE'])
@db_connect
def positions():
    db_cursor = g.db_conn.cursor()
    if request.method == 'GET':
        db_cursor.execute('SELECT * FROM t_position')
        positions = get_positions_list(positions=db_cursor.fetchall())

        return render_template('positions.html', positions=positions)


@app.route('/subjects', methods=['GET', 'POST'])
@db_connect
def subjects():
    db_cursor = g.db_conn.cursor()

    if request.method == 'GET':
        db_cursor.execute('SELECT * FROM t_subject;')
        subject_list = db_cursor.fetchall()
        subjects = get_subjects_list(subjects=subject_list)

        return render_template('subjects.html', subjects=subjects)
    elif request.method == 'POST':
        subject_name = request.json.get('subject_name')
        db_cursor.execute('INSERT INTO t_subject (name) VALUES(%s)', (subject_name,))

        return {'status': 'OK'}


# API for service

# @app.route('/api/v1/groups', methods=['GET', 'POST'])
# @db_connect
# def groups():
#     db_cursor = g.db_conn.cursor()

#     if request.method == 'GET':
#         db_cursor.execute('SELECT * FROM t_group')
#         group_list = db_cursor.fetchall()
#         groups = get_group_list(groups=group_list)    

#         return {'list': groups}

#     elif request.method == 'POST':
#         group_name = request.json.get('group_name')
#         db_cursor.execute('INSERT INTO t_group (name) VALUES (%s)', (group_name,))

#         return {'status': 'CREATED'}


# @app.route('/api/v1/groups/<int:group_id>', methods=['GET', 'PUT', 'DELETE'])
# @db_connect
# def group_detail(group_id):
#     db_cursor = g.db_conn.cursor()

#     if request.method == 'GET':
#         db_cursor.execute(f'SELECT * FROM t_group WHERE id={group_id}')
#         group = db_cursor.fetchone()

#         return {'id': group[0], 'name': group[1]}
#     elif request.method == 'PUT':
#         group_name = request.json.get('group_name')
        

app.run(host='127.0.0.1', port=8000, debug=True)
