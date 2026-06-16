from flask import Flask, send_from_directory
from flask_jwt_extended import JWTManager
from models import db, bcrypt, ProjectCategory
from auth import auth_bp
from routes import api_bp
from swagger import swaggerui_blueprint, SWAGGER_URL
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    JWTManager(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    @app.route('/static/<path:path>')
    def send_static(path):
        return send_from_directory('static', path)

    # Test route to confirm server is running
    @app.route('/')
    def home():
        return 'Server is running!', 200

    with app.app_context():
        db.create_all()
        default_categories = [
            'Web Development', 'Mobile Development', 'Graphic Design', 'Data Analysis']
        for cat_name in default_categories:
            if not ProjectCategory.query.filter_by(name=cat_name).first():
                db.session.add(ProjectCategory(name=cat_name))
        db.session.commit()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
