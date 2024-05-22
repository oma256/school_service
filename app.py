from flask import Flask, render_template
from database import conn

from groups import get_group_list
from students import get_students_list


app = Flask(__name__)


@app.route('/groups', methods=['GET'])
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
