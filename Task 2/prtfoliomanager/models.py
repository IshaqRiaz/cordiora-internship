from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    portfolio = db.relationship('Portfolio', backref='user', uselist=False)
    projects = db.relationship('Project', backref='owner', lazy='dynamic')
    skills = db.relationship('Skill', backref='owner', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(
            password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    full_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    location = db.Column(db.String(200))
    title = db.Column(db.String(200))

    about = db.Column(db.Text)
    experience_years = db.Column(db.Integer)

    contact_email = db.Column(db.String(100))
    contact_phone = db.Column(db.String(20))

    github = db.Column(db.String(200))
    linkedin = db.Column(db.String(200))
    twitter = db.Column(db.String(200))
    website = db.Column(db.String(200))

    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ProjectCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(200))
    projects = db.relationship('Project', backref='category', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'project_count': self.projects.count()
        }


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'project_category.id'), nullable=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    technologies = db.Column(db.String(250), nullable=True)
    github_link = db.Column(db.String(200))
    live_link = db.Column(db.String(200))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'technologies': self.technologies,
            'category': self.category.name if self.category else None,
            'github_link': self.github_link,
            'live_link': self.live_link,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None
        }


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    proficiency = db.Column(db.Integer)
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'proficiency': self.proficiency,
            'category': self.category
        }
