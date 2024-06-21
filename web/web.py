from flask import Blueprint, request, render_template
from helpers import (
    get_index_page_data, get_group_list, get_students_list,
    get_positions_list, get_teachers_list, get_subjects_list,
)
from models import (
    db, TeacherGroupSubject, Student, Group, Teacher, Subject, User
)


web_page = Blueprint('web', __name__, template_folder='templates')


@web_page.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = db.session.query(User).filter(
            User.email == request.form.get('email')
        ).first()

        print(user.first_name)
        print(user.last_name)
        print(user.email)
        print(user.phone_number)
        print(user.password)

    return render_template('login.html')


@web_page.route('/', methods=['GET', 'POST', 'DELETE', 'PUT'])
def index():

    if request.method == 'GET':
        data = get_index_page_data()
        return render_template(template_name_or_list='index.html', 
                               data=data)
    
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
    

@web_page.route('/students', methods=['GET', 'POST', 'PUT', 'DELETE'])
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
    

@web_page.route('/groups', methods=['GET', 'POST', 'DELETE', 'PUT'])
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


@web_page.route('/teachers', methods=['GET', 'POST', 'DELETE', 'PUT'])
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
    

@web_page.route('/positions', methods=['GET', 'POST', 'PUT', 'DELETE'])
def positions():
    if request.method == 'GET':
        positions = get_positions_list()

        return render_template('positions.html', positions=positions)
    

@web_page.route('/subjects', methods=['GET', 'POST', 'DELETE', 'PUT'])
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
