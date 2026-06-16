from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Project, Skill, Portfolio, ProjectCategory
from datetime import datetime
from sqlalchemy import or_

api_bp = Blueprint('api', __name__)

# ==================== PORTFOLIO ====================


@api_bp.route('/portfolio', methods=['GET', 'PUT'])
@jwt_required()
def manage_portfolio():
    user_id = get_jwt_identity()
    portfolio = Portfolio.query.filter_by(user_id=user_id).first()

    if request.method == 'GET':
        if not portfolio:
            return jsonify({'message': 'Portfolio not found'}), 404
        return jsonify({
            'full_name': portfolio.full_name,
            'email': portfolio.email,
            'phone': portfolio.phone,
            'location': portfolio.location,
            'title': portfolio.title,
            'about': portfolio.about,
            'experience_years': portfolio.experience_years,
            'contact_email': portfolio.contact_email,
            'contact_phone': portfolio.contact_phone,
            'github': portfolio.github,
            'linkedin': portfolio.linkedin,
            'twitter': portfolio.twitter,
            'website': portfolio.website
        }), 200

    data = request.get_json()
    if not portfolio:
        portfolio = Portfolio(user_id=user_id)
        db.session.add(portfolio)

    portfolio.full_name = data.get('full_name', portfolio.full_name)
    portfolio.email = data.get('email', portfolio.email)
    portfolio.phone = data.get('phone', portfolio.phone)
    portfolio.location = data.get('location', portfolio.location)
    portfolio.title = data.get('title', portfolio.title)
    portfolio.about = data.get('about', portfolio.about)
    portfolio.experience_years = data.get(
        'experience_years', portfolio.experience_years)
    portfolio.contact_email = data.get(
        'contact_email', portfolio.contact_email)
    portfolio.contact_phone = data.get(
        'contact_phone', portfolio.contact_phone)
    portfolio.github = data.get('github', portfolio.github)
    portfolio.linkedin = data.get('linkedin', portfolio.linkedin)
    portfolio.twitter = data.get('twitter', portfolio.twitter)
    portfolio.website = data.get('website', portfolio.website)

    db.session.commit()
    return jsonify({'message': 'Portfolio updated successfully'}), 200

# ==================== SKILLS ====================


@api_bp.route('/skills', methods=['GET', 'POST'])
@jwt_required()
def handle_skills():
    user_id = get_jwt_identity()

    if request.method == 'GET':
        skills = Skill.query.filter_by(user_id=user_id).all()
        return jsonify([skill.to_dict() for skill in skills]), 200

    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'message': 'Skill name required'}), 400

    skill = Skill(
        user_id=user_id,
        name=data['name'],
        proficiency=data.get('proficiency', 50),
        category=data.get('category')
    )
    db.session.add(skill)
    db.session.commit()
    return jsonify({'message': 'Skill added', 'skill': skill.to_dict()}), 201


@api_bp.route('/skills/<int:skill_id>', methods=['PUT', 'DELETE'])
@jwt_required()
def manage_skill(skill_id):
    user_id = get_jwt_identity()
    skill = Skill.query.filter_by(id=skill_id, user_id=user_id).first()
    if not skill:
        return jsonify({'message': 'Skill not found'}), 404

    if request.method == 'DELETE':
        db.session.delete(skill)
        db.session.commit()
        return jsonify({'message': 'Skill deleted'}), 200

    data = request.get_json()
    skill.name = data.get('name', skill.name)
    skill.proficiency = data.get('proficiency', skill.proficiency)
    skill.category = data.get('category', skill.category)
    db.session.commit()
    return jsonify({'message': 'Skill updated', 'skill': skill.to_dict()}), 200

# ==================== CATEGORIES ====================


@api_bp.route('/categories', methods=['GET', 'POST'])
@jwt_required()
def handle_categories():
    if request.method == 'GET':
        categories = ProjectCategory.query.all()
        return jsonify([cat.to_dict() for cat in categories]), 200

    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'message': 'Category name required'}), 400

    if ProjectCategory.query.filter_by(name=data['name']).first():
        return jsonify({'message': 'Category already exists'}), 409

    category = ProjectCategory(
        name=data['name'], description=data.get('description'))
    db.session.add(category)
    db.session.commit()
    return jsonify({'message': 'Category created', 'category': category.to_dict()}), 201


@api_bp.route('/categories/<int:category_id>', methods=['PUT', 'DELETE'])
@jwt_required()
def manage_category(category_id):
    category = ProjectCategory.query.get(category_id)
    if not category:
        return jsonify({'message': 'Category not found'}), 404

    if request.method == 'DELETE':
        Project.query.filter_by(category_id=category_id).update(
            {'category_id': None})
        db.session.delete(category)
        db.session.commit()
        return jsonify({'message': 'Category deleted'}), 200

    data = request.get_json()
    category.name = data.get('name', category.name)
    category.description = data.get('description', category.description)
    db.session.commit()
    return jsonify({'message': 'Category updated', 'category': category.to_dict()}), 200

# ==================== SEARCH ====================


@api_bp.route('/projects/search', methods=['GET'])
@jwt_required()
def search_projects():
    user_id = get_jwt_identity()
    query = request.args.get('q', '')
    technology = request.args.get('tech', '')
    category_name = request.args.get('category', '')

    projects_query = Project.query.filter_by(user_id=user_id)

    if query:
        projects_query = projects_query.filter(
            or_(
                Project.name.ilike(f'%{query}%'),
                Project.description.ilike(f'%{query}%')
            )
        )

    if technology:
        projects_query = projects_query.filter(
            Project.technologies.ilike(f'%{technology}%')
        )

    if category_name:
        projects_query = projects_query.join(ProjectCategory).filter(
            ProjectCategory.name.ilike(f'%{category_name}%')
        )

    projects = projects_query.all()
    return jsonify([project.to_dict() for project in projects]), 200

# ==================== DASHBOARD STATS ====================


@api_bp.route('/dashboard/stats', methods=['GET'])
@jwt_required()
def dashboard_stats():
    user_id = get_jwt_identity()

    total_projects = Project.query.filter_by(user_id=user_id).count()
    total_skills = Skill.query.filter_by(user_id=user_id).count()

    categories = ProjectCategory.query.all()
    category_counts = {}
    for cat in categories:
        count = Project.query.filter_by(
            user_id=user_id, category_id=cat.id).count()
        if count > 0:
            category_counts[cat.name] = count

    skills_by_category = {}
    skills = Skill.query.filter_by(user_id=user_id).all()
    for skill in skills:
        cat = skill.category or 'Uncategorized'
        skills_by_category.setdefault(cat, []).append(skill.name)

    return jsonify({
        'total_projects': total_projects,
        'total_skills': total_skills,
        'category_counts': category_counts,
        'skills_by_category': skills_by_category
    }), 200

# ==================== PROJECT CRUD ====================


@api_bp.route('/projects', methods=['GET'])
@jwt_required()
def get_all_projects():
    user_id = get_jwt_identity()
    projects = Project.query.filter_by(user_id=user_id).all()
    return jsonify([project.to_dict() for project in projects]), 200


@api_bp.route('/projects', methods=['POST'])
@jwt_required()
def add_project():
    user_id = get_jwt_identity()
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'message': 'Project name required'}), 400

    category_id = None
    if data.get('category'):
        category = ProjectCategory.query.filter_by(
            name=data['category']).first()
        if category:
            category_id = category.id

    def parse_date(date_str):
        return datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

    project = Project(
        user_id=user_id,
        name=data['name'],
        description=data.get('description'),
        technologies=data.get('technologies'),
        category_id=category_id,
        github_link=data.get('github_link'),
        live_link=data.get('live_link'),
        start_date=parse_date(data.get('start_date')),
        end_date=parse_date(data.get('end_date'))
    )
    db.session.add(project)
    db.session.commit()
    return jsonify({'message': 'Project created', 'project': project.to_dict()}), 201


@api_bp.route('/projects/<int:project_id>', methods=['PUT'])
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
    project.github_link = data.get('github_link', project.github_link)
    project.live_link = data.get('live_link', project.live_link)

    if data.get('category'):
        category = ProjectCategory.query.filter_by(
            name=data['category']).first()
        project.category_id = category.id if category else None

    def parse_date(date_str):
        return datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

    if data.get('start_date'):
        project.start_date = parse_date(data['start_date'])
    if data.get('end_date'):
        project.end_date = parse_date(data['end_date'])

    db.session.commit()
    return jsonify({'message': 'Project updated', 'project': project.to_dict()}), 200


@api_bp.route('/projects/<int:project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    user_id = get_jwt_identity()
    project = Project.query.filter_by(id=project_id, user_id=user_id).first()
    if not project:
        return jsonify({'message': 'Project not found'}), 404

    db.session.delete(project)
    db.session.commit()
    return jsonify({'message': 'Project deleted'}), 200
