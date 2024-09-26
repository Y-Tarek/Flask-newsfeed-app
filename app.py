from flask import Flask, request, jsonify
from models import create_tables


def create_app():

    app = Flask(__name__)
    app.cli.add_command(create_tables)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

