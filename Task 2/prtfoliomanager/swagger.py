from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'  # This is the URL where Swagger UI will be available
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Portfolio Manager API"
    }
)
