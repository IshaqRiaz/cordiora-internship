from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Project

project_bp = Blueprint('projects', __name__)


@project_bp.route('/projects', methods=['GET'])
@jwt_required()
def list_projects():
    user_id = get_jwt_identity()
    projects = Project.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'technologies': p.technologies
    } for p in projects]), 200


@project_bp.route('/projects', methods=['POST'])
@jwt_required()
def add_project():
    user_id = get_jwt_identity()
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'message': 'Project name required'}), 400
    project = Project(
        user_id=user_id,
        name=data['name'],
        description=data.get('description'),
        technologies=data.get('technologies')
    )
    db.session.add(project)
    db.session.commit()
    return jsonify({'message': 'Project created', 'id': project.id}), 201


@project_bp.route('/projects/<int:project_id>', methods=['PUT'])
@jwt_required()
def update_project(project_id):
    user_id = get_jwt_identity()
    project = Project.query.filter_by(id=project_id, user_id=user_id).first()
    if not project:
        return jsonify({'message': 'Project not found'}), 404
    data = request.get_json()
    project.name = data.get('name', project.name)
    project.description = data.get('description', project.description)
    project.technologies = data.get('technologies', project.technologies)
    db.session.commit()
    return jsonify({'message': 'Project updated'}), 200


@project_bp.route('/projects/<int:project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    user_id = get_jwt_identity()
    project = Project.query.filter_by(id=project_id, user_id=user_id).first()
    if not project:
        return jsonify({'message': 'Project not found'}), 404
    db.session.delete(project)
    db.session.commit()
    return jsonify({'message': 'Project deleted'}), 200
