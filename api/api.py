from flask import Blueprint, request

from helpers import get_group_list
from models import db, Group


api_bp = Blueprint('api', __name__, url_prefix='/api/v1')


@api_bp.route('/groups', methods=['GET', 'POST'])
def groups():
    if request.method == 'GET':
        groups = get_group_list()    

        return {'list': groups}

    elif request.method == 'POST':
        group_name = request.json.get('group_name')
        group = Group(name=group_name)
        db.session.add(group)
        db.session.commit()

        return {'status': 'CREATED'}
    

@api_bp.route('/groups/<int:group_id>', methods=['GET', 'PUT', 'DELETE'])
def group_detail(group_id):

    if request.method == 'GET':
        group = db.session.query(Group).filter(Group.id == group_id).first()

        return {'id': group.id, 'name': group.name}

    elif request.method == 'PUT':
        group_name = request.json.get('group_name')