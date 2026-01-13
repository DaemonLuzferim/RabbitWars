from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from auth import auth
from posts import posts

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
db.init_app(app)
JWTManager(app)

app.register_blueprint(auth, url_prefix="/api")
app.register_blueprint(posts, url_prefix="/api")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()
