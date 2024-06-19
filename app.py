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
from models import Group, Student, Subject, Teacher, db, TeacherGroupSubject
from utils import create_app


app = create_app()


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/', methods=['GET', 'POST', 'DELETE', 'PUT'])
def index():

    if request.method == 'GET':
        data = get_index_page_data()
        return render_template(template_name_or_list='index.html', data=data)
    
    elif request.method == 'POST':
        teacher_id = int(request.json.get('teacher_id'))
        group_id = int(request.json.get('group_id'))
        subject_id = int(request.json.get('subject_id'))

        teacher_group_subject = TeacherGroupSubject(
            teacher_id=teacher_id,
            group_id=group_id,
            subject_id=subject_id,
        )
        db.session.add(teacher_group_subject)
        db.session.commit()

        return {'status': 'OK'}

    elif request.method == 'DELETE':
        item_id = int(request.json.get('item_id'))

        db.session.query(TeacherGroupSubject).filter(
            TeacherGroupSubject.id == item_id
        ).delete()

        db.session.commit()

        return {'status': 'OK'}

    elif request.method == 'PUT':
        teacher_id = int(request.json.get('teacher_id'))
        group_id = int(request.json.get('group_id'))
        subject_id = int(request.json.get('subject_id'))
        data_id = int(request.json.get('data_id'))

        teacher_group_subject = db.session.query(TeacherGroupSubject).filter(
            TeacherGroupSubject.id == data_id
        ).first()

        teacher_group_subject.teacher_id = teacher_id
        teacher_group_subject.group_id = group_id
        teacher_group_subject.subject_id = subject_id

        db.session.add(teacher_group_subject)
        db.session.commit()

        return {'status': 'OK'}


@app.route('/students', methods=['GET', 'POST', 'PUT', 'DELETE'])
def students():
    if request.method == 'GET':
        if request.args.get('group_id'):
            students = db.session.query(Student).filter(
                Student.group_id == int(request.args.get('group_id'))
            ).all()
        else:
            students = db.session.query(Student).all()

        students = get_students_list(students=students)
        groups = get_group_list()

        return render_template('students.html', students=students, groups=groups)

    elif request.method == 'POST':
        student = Student(
            first_name = request.json.get('first_name'),
            last_name = request.json.get('last_name'),
            group_id = int(request.json.get('group_id'))
        )
        db.session.add(student)
        db.session.commit()

        return {'status': 'OK'}
    
    elif request.method == 'PUT':
        student = db.session.query(Student).filter(
            Student.id == int(request.json.get('student_id'))
        ).first()

        student.first_name = request.json.get('first_name')
        student.last_name = request.json.get('last_name')
        student.group_id = int(request.json.get('group_id'))

        db.session.commit()

        return {'status': 'OK'}

    elif request.method == 'DELETE':
        try:
            student = db.session.query(Student).filter(
                Student.id == int(request.json.get('student_id'))
            ).first()
            db.session.delete(student)
            db.session.commit()
        except Exception as e:
            return {'status': 'FAILED'}

        return {'status': 'OK'}


@app.route('/groups', methods=['GET', 'POST', 'DELETE', 'PUT'])
def groups():
    if request.method == 'GET':
        groups = get_group_list()
        return render_template('groups.html', groups=groups)

    elif request.method == 'POST':
        group_name = request.json.get('group_name')

        group = db.session.query(Group).filter(
            Group.name == group_name
        ).first()

        if group:
            return {'status': 'FAILED'}
        else:
            group = Group(name=group_name)
            db.session.add(group)
            db.session.commit()
            return {'status': 'OK'}
    
    elif request.method == 'DELETE':
        group = db.session.query(Group).filter(
            Group.id == int(request.json.get('group_id'))
        ).first()
        db.session.delete(group)
        db.session.commit()

        return {'status': 'OK'}
    
    elif request.method == 'PUT':
        group = db.session.query(Group).filter(
            Group.id == int(request.json.get('group_id'))
        ).first()
        group.name = request.json.get('group_name')
        db.session.add(group)
        db.session.commit()

        return {'status': 'OK'}


@app.route('/teachers', methods=['GET', 'POST', 'DELETE', 'PUT'])
def teachers():
    if request.method == 'GET':
        teachers = get_teachers_list()
        positions = get_positions_list()

        return render_template('teachers.html', 
                               teachers=teachers, 
                               positions=positions)

    elif request.method == 'POST':
        teacher = Teacher(
            first_name = request.json.get('first_name'),
            last_name = request.json.get('last_name'),
            position_id = int(request.json.get('position_id'))
        )

        db.session.add(teacher)
        db.session.commit()

        return {'status': 'OK'}

    elif request.method == 'DELETE':
        teacher = db.session.query(Teacher).filter(
            Teacher.id == int(request.json.get('teacher_id'))
        ).first()

        db.session.delete(teacher)
        db.session.commit()

        return {'status': 'OK'}

    elif request.method == 'PUT':
        teacher = db.session.query(Teacher).filter(
            Teacher.id == int(request.json.get('teacher_id'))
        ).first()

        teacher.first_name = request.json.get('first_name')
        teacher.last_name = request.json.get('last_name')
        teacher.position_id = int(request.json.get('position_id'))

        db.session.commit()

        return {'status': 'OK'}


@app.route('/positions', methods=['GET', 'POST', 'PUT', 'DELETE'])
@db_connect
def positions():
    db_cursor = g.db_conn.cursor()
    if request.method == 'GET':
        db_cursor.execute('SELECT * FROM t_position')
        positions = get_positions_list(positions=db_cursor.fetchall())

        return render_template('positions.html', positions=positions)


@app.route('/subjects', methods=['GET', 'POST', 'DELETE', 'PUT'])
def subjects():
    if request.method == 'GET':
        subjects = get_subjects_list()
        return render_template('subjects.html', subjects=subjects)

    elif request.method == 'POST':
        subject_name = request.json.get('subject_name')
        subject = Subject(name=subject_name)
        
        db.session.add(subject)
        db.session.commit()

        return {'status': 'OK'}

    elif request.method == 'DELETE':
        subject = db.session.query(Subject).filter(
            Subject.id == int(request.json.get('subject_id'))
        ).first()
        db.session.delete(subject)
        db.session.commit()

        return {'status': 'OK'}

    elif request.method == 'PUT':
        subject = db.session.query(Subject).filter(
            Subject.id == int(request.json.get('subject_id'))
        ).first()

        subject.name = request.json.get('subject_name')
        db.session.commit()

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
        

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)
