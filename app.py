from flask import Flask, render_template, g, request
from flask_cors import CORS
from database import db_connect

from helpers import (
    get_group_list,
    get_students_list,
    get_subjects_list,
    get_teachers_list,
    get_teachers_groups_list,
)


app = Flask(__name__)
CORS(app=app)


# @app.route('/groups', methods=['GET', 'POST'])
# @db_connect
# def get_groups():
#     db_cursor = g.db_conn.cursor()
    
#     if request.method == 'GET':
#         db_cursor.execute('SELECT * FROM t_group;')
#         group_list = db_cursor.fetchall()
#         groups = get_group_list(groups=group_list)

#         return render_template('groups.html', groups=groups)
#     elif request.method == 'POST':
#         group_name = request.json.get('group_name')
#         db_cursor.execute('INSERT INTO t_group (name) VALUES (%s)', (group_name,))

#         return {'status': 'OK'}

# @app.route('/students', methods=['GET', 'POST'])
# @db_connect
# def get_students():
#     db_cursor = g.db_conn.cursor()

#     if request.method == 'GET':
#         db_cursor.execute('SELECT * FROM t_student')
#         student_list = db_cursor.fetchall()
#         students = get_students_list(students=student_list)

#         db_cursor.execute('SELECT * FROM t_group')
#         group_list = db_cursor.fetchall()
#         groups = get_group_list(groups=group_list)


#         return render_template('students.html', students=students, groups=groups)
#     elif request.method == 'POST':
#         first_name = request.json.get('first_name')
#         last_name = request.json.get('last_name')
#         group_id = int(request.json.get('group_id'))

#         db_cursor.execute(
#             'INSERT INTO t_student (first_name, last_name, group_id) VALUES (%s, %s, %s)', 
#             (first_name, last_name, group_id))

#         return {'status': 'OK'}



# @app.route('/teachers', methods=['GET'])
# @db_connect
# def get_teachers():
#     db_cursor = g.db_conn.cursor()
#     db_cursor.execute('SELECT * FROM t_teacher;')
#     teacher_list = db_cursor.fetchall()
#     teachers = get_teachers_list(teachers=teacher_list)

#     return render_template('teachers.html', teachers=teachers)


# @app.route('/subjects', methods=['GET', 'POST'])
# @db_connect
# def get_subjects():
#     db_cursor = g.db_conn.cursor()

#     if request.method == 'GET':
#         db_cursor.execute('SELECT * FROM t_subject;')
#         subject_list = db_cursor.fetchall()
#         subjects = get_subjects_list(subjects=subject_list)

#         return render_template('subjects.html', subjects=subjects)
#     elif request.method == 'POST':
#         subject_name = request.json.get('subject_name')
#         db_cursor.execute('INSERT INTO t_subject (name) VALUES(%s)', (subject_name,))

#         return {'status': 'OK'}

# @app.route('/teachers_groups', methods=['GET'])
# @db_connect
# def get_teachers_groups():
#     db_cursor = g.db_conn.cursor()
#     db_cursor.execute('SELECT * FROM t_teachers_groups_subjects;')
#     teachers_groups_list = db_cursor.fetchall()
#     teachers_groups = get_teachers_groups_list(
#         teachers_groups=teachers_groups_list
#     )

#     return render_template('teachers_groups.html', 
#                            teachers_groups=teachers_groups)


# API for service

@app.route('/api/v1/groups', methods=['GET', 'POST'])
@db_connect
def groups():
    db_cursor = g.db_conn.cursor()

    if request.method == 'GET':
        db_cursor.execute('SELECT * FROM t_group')
        group_list = db_cursor.fetchall()
        groups = get_group_list(groups=group_list)    

        return {'list': groups}

    elif request.method == 'POST':
        group_name = request.json.get('group_name')
        db_cursor.execute('INSERT INTO t_group (name) VALUES (%s)', (group_name,))

        return {'status': 'CREATED'}


@app.route('/api/v1/groups/<int:group_id>', methods=['GET', 'PUT', 'DELETE'])
@db_connect
def group_detail(group_id):
    db_cursor = g.db_conn.cursor()

    if request.method == 'GET':
        db_cursor.execute(f'SELECT * FROM t_group WHERE id={group_id}')
        group = db_cursor.fetchone()

        return {'id': group[0], 'name': group[1]}
    elif request.method == 'PUT':
        group_name = request.json.get('group_name')
        

app.run(host='127.0.0.1', port=5000, debug=True)
