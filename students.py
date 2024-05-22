def get_students_list(students):
    result = []

    for student in students:
        result.append({
            'id': student[0], 
            'first_name': student[1],
            'last_name': student[2],
            'group_id': student[3]
        })
    
    return result
