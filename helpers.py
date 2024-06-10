from flask import g


def get_index_page_data():
    db_cursor = g.db_conn.cursor()

    db_cursor.execute('SELECT * FROM t_teacher')
    teachers = get_teachers_list(teachers=db_cursor.fetchall())

    db_cursor.execute('SELECT * FROM t_group')
    groups = get_group_list(groups=db_cursor.fetchall())

    db_cursor.execute('SELECT * FROM t_subject')
    subjects = get_subjects_list(subjects=db_cursor.fetchall())


    data = {
        'teachers': teachers,
        'groups': groups,
        'subjects': subjects,
    }

    result = []
    db_cursor.execute('SELECT * FROM t_teachers_groups_subjects')
    teachers_groups_subjects = db_cursor.fetchall()

    for teacher_group_subject in teachers_groups_subjects:
        db_cursor.execute('SELECT * FROM t_teacher WHERE id=%s', 
                          (teacher_group_subject[1],))
        teacher = db_cursor.fetchone()

        db_cursor.execute('SELECT * FROM t_position WHERE id=%s',
                          (teacher[3],))
        position = db_cursor.fetchone()

        db_cursor.execute('SELECT * FROM t_group WHERE id=%s',
                          (teacher_group_subject[2],))
        group = db_cursor.fetchone()

        db_cursor.execute('SELECT * FROM t_subject WHERE id=%s',
                          (teacher_group_subject[3],))
        subject = db_cursor.fetchone()

        result.append({
            'id': teacher_group_subject[0],
            'teacher_id': teacher[0],
            'teacher_fullname': f'{teacher[1]} {teacher[2]} ({position[1]})',
            'group_id': group[0],
            'group_name': group[1],
            'subject_id': subject[0],
            'subject_name': subject[1],
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
