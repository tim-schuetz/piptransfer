from flask import Flask
from flask_cors import CORS
from .routes import all_blueprints
from .models import db

def create_app():
    
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dmsdata.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    with app.app_context():
        db.create_all()

    for bp in all_blueprints:
        app.register_blueprint(bp)

    return app 


