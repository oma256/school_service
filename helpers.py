from flask import g

from models import (
    db, Teacher, Group, Subject, TeacherGroupSubject, Position
)


def get_index_page_data():
    teachers = db.session.query(Teacher).all()
    groups = db.session.query(Group).all()
    subjects = db.session.query(Subject).all()

    data = {
        'teachers': teachers,
        'groups': groups,
        'subjects': subjects,
    }

    result = []
    teachers_groups_subjects = db.session.query(TeacherGroupSubject).all()

    for teacher_group_subject in teachers_groups_subjects:
        teacher = db.session.query(Teacher).filter(
            Teacher.id == teacher_group_subject.teacher_id
        ).first()

        position = db.session.query(Position).filter(
            Position.id == teacher.position_id
        ).first()

        group = db.session.query(Group).filter(
            Group.id == teacher_group_subject.group_id
        ).first()

        subject = db.session.query(Subject).filter(
            Subject.id == teacher_group_subject.subject_id
        ).first()

        result.append({
            'id': teacher_group_subject.id,
            'teacher_id': teacher.id,
            'teacher_fullname': f'{teacher.first_name} {teacher.last_name} ({position.name})',
            'group_id': group.id,
            'group_name': group.name,
            'subject_id': subject.id,
            'subject_name': subject.name,
        })

    data['list'] = result

    return data


def get_group_list(groups):
    result = []

    for group in groups:
        result.append({'id': group[0], 'name': group[1]})
    
    return result


def get_students_list(students):
    result = []
    db_cursor = g.db_conn.cursor()

    for student in students:
        db_cursor.execute(f'SELECT * FROM t_group WHERE id={student[3]}')
        group = db_cursor.fetchone()

        result.append({
            'id': student[0], 
            'first_name': student[1],
            'last_name': student[2],
            'group_name': group[1],
            'group_id': group[0],
        })

    return result


def get_teachers_list(teachers):
    result = []
    db_cursor = g.db_conn.cursor()

    for teacher in teachers:
        db_cursor.execute(f'SELECT * FROM t_position WHERE id={teacher[3]}')
        position = db_cursor.fetchone()

        result.append({
            'id': teacher[0],
            'first_name': teacher[1],
            'last_name': teacher[2],
            'position_name': position[1],
            'position_id': position[0],
        })

    return result


def get_subjects_list(subjects):
    result = []

    for subject in subjects:
        result.append({'id': subject[0], 'name': subject[1]})

    return result


def get_positions_list(positions):
    result = []

    for position in positions:
        result.append({'id': position[0], 'name': position[1]})
    
    return result
