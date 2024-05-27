from flask import Flask, render_template
from database import conn

from helpers import (
    get_group_list,
    get_students_list,
    get_subjects_list,
    get_teachers_list,
    get_teachers_groups_list,
)


app = Flask(__name__)


@app.route('/groups', methods=['GET', 'POST'])
def get_groups():
    con = conn.cursor()
    con.execute('SELECT * FROM t_group;')
    group_list = con.fetchall()
    groups = get_group_list(groups=group_list)

    return render_template('groups.html', groups=groups)


@app.route('/students', methods=['GET'])
def get_students():
    con = conn.cursor()
    con.execute('SELECT * FROM t_student;')
    student_list = con.fetchall()
    students = get_students_list(students=student_list)

    return render_template('students.html', students=students)


@app.route('/teachers', methods=['GET'])
def get_teachers():
    con = conn.cursor()
    con.execute('SELECT * FROM t_teacher;')
    teacher_list = con.fetchall()
    teachers = get_teachers_list(teachers=teacher_list)

    return render_template('teachers.html', teachers=teachers)


@app.route('/subjects', methods=['GET'])
def get_subjects():
    con = conn.cursor()
    con.execute('SELECT * FROM t_subject;')
    subject_list = con.fetchall()
    subjects = get_subjects_list(subjects=subject_list)

    return render_template('subjects.html', subjects=subjects)


@app.route('/teachers_groups', methods=['GET'])
def get_teachers_groups():
    con = conn.cursor()
    con.execute('SELECT * FROM t_teachers_groups_subjects;')
    teachers_groups_list = con.fetchall()
    teachers_groups = get_teachers_groups_list(
        teachers_groups=teachers_groups_list
    )

    return render_template('teachers_groups.html', 
                           teachers_groups=teachers_groups)
