from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)

from helpers import check_password, get_group_list, get_positions_list, get_teachers_list
from models import Position, Teacher, User, db, Group


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


@api_bp.route('/positions', methods=['GET', 'POST'])
@jwt_required()
def positions():
    
    if request.method == 'GET':
        positions = get_positions_list()

        return {'list': positions}

    elif request.method == 'POST':
        position_name = request.json.get('name')
        position = db.session.query(Position).filter(
            Position.name == position_name
        ).first()

        if position:
            return jsonify(
                {'status': 'FAILED', 'message': 'position already exist'}
            ), 400

        position = Position(name=position_name)
        db.session.add(position)
        db.session.commit()

        return jsonify(
            {'status': 'SUCCESS', 'message': 'position created'}
        ), 201
    

@api_bp.route('/positions/<int:position_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def position_detail(position_id):

    position = db.session.query(Position).filter(
        Position.id == position_id
    ).first()

    if not position:
        return jsonify(
            {'status': 'FAILED', 'message': 'position not found'},
        ), 400

    if request.method == 'GET':
        return jsonify({'id': position.id, 'name': position.name}), 200

    elif request.method == 'DELETE':
        db.session.delete(position)
        db.session.commit()

        return jsonify({'status': 'SUCCESS', 'message': 'position deleted'}), 200

    elif request.method == 'PUT':
        position.name = request.json.get('name')
        db.session.commit()

        return jsonify({'status': 'SUCCESS', 'message': 'position edited'}), 200


@api_bp.route('/teachers', methods=['GET', 'POST'])
@jwt_required()
def teachers():

    if request.method == 'GET':
        teachers = get_teachers_list()
        return {'list': teachers}

    elif request.method == 'POST':
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        position_id = request.json.get('position_id')

        teacher = Teacher(
            first_name=first_name,
            last_name=last_name,
            position_id=position_id
        )
        db.session.add(teacher)
        db.session.commit()

        return jsonify(
            {'status': 'SUCCESS', 'message': 'teacher created'}
        ), 201


@api_bp.route('/teachers/<int:teacher_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def teacher_detail(teacher_id):

    teacher = db.session.query(Teacher).filter(
        Teacher.id == teacher_id
    ).first()

    if not teacher:
        return jsonify(
            {'status': 'FAILED', 'message': 'teacher not found'},
        ), 400

    if request.method == 'GET':
        return jsonify({
            'id': teacher.id, 
            'first_name': teacher.first_name,
            'last_name': teacher.last_name,
            'position_id': teacher.position_id
        }), 200

    elif request.method == 'DELETE':
        db.session.delete(teacher)
        db.session.commit()

        return jsonify({'status': 'SUCCESS', 'message': 'teacher deleted'}), 200

    elif request.method == 'PUT':
        teacher.first_name = request.json.get('first_name')
        teacher.last_name = request.json.get('last_name')
        teacher.position_id = request.json.get('position_id')
        db.session.commit()

        return jsonify({'status': 'SUCCESS', 'message': 'teacher edited'}), 200