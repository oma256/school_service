def get_group_list(groups):
    result = []

    for group in groups:
        result.append({'id': group[0], 'name': group[1]})
    
    return result
