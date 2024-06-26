from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)

from helpers import check_password, get_group_list
from models import User, db, Group


api_bp = Blueprint('api', __name__, url_prefix='/api/v1')


@api_bp.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    user = db.session.query(User).filter(User.email == email).first()

    if user and check_password(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({'message': 'Login Success', 'access_token': access_token})
    else:
        return jsonify({'message': 'Login Failed'}), 401


@api_bp.route('/groups', methods=['GET', 'POST'])
@jwt_required()
def groups():
    if request.method == 'GET':
        groups = get_group_list()    

        return {'list': groups}

    elif request.method == 'POST':
        group_name = request.json.get('group_name')
        
        group = db.session.query(Group).filter(
            Group.name == group_name
        ).first()

        if group:
            return {'status': 'FAILED', 'message': 'group alredy exist'}

        group = Group(name=group_name)
        db.session.add(group)
        db.session.commit()

        return {'status': 'CREATED', 'message': f'group {group_name} created'}


@api_bp.route('/groups/<int:group_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def group_detail(group_id):

    if request.method == 'GET':
        group = db.session.query(Group).filter(Group.id == group_id).first()

        if not group:
            return {'status': 'FAILED', 'message': 'group not found'}

        return {'id': group.id, 'name': group.name}

    elif request.method == 'DELETE':
        group = db.session.query(Group).filter(
            Group.id == group_id
        ).first()

        if not group:
            return {'status': 'FAILED', 'message': 'group not found'}

        db.session.delete(group)
        db.session.commit()

        return {'status': 'SUCCESS', 'message': 'group is deleted'}

    elif request.method == 'PUT':
        group = db.session.query(Group).filter(Group.id == group_id).first()

        if not group:
            return {'status': 'FAILED', 'message': 'group not found'}

        group.name = request.json.get('group_name')

        db.session.add(group)
        db.session.commit()

        return {'status': 'SUCCESS', 'message': 'group is updated'}
