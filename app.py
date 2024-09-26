from flask import Flask
from models import create_tables
from flask_jwt_extended import JWTManager
from auth import auth_bp
from posts import posts_bp
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.cli.add_command(create_tables)
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
    jwt = JWTManager(app)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(posts_bp, url_prefix='/posts')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

