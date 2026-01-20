from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

# =========================
# CONFIGURACIÓN
# =========================
app = Flask(__name__)
CORS(app)

app.config["JWT_SECRET_KEY"] = "super-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

db = SQLAlchemy(app)
jwt = JWTManager(app)

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# =========================
# MODELO USUARIO
# =========================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

# =========================
# REGISTRO
# =========================
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify(msg="Completa todos los campos"), 400

    if User.query.filter_by(email=email).first():
        return jsonify(msg="El usuario ya existe"), 400

    user = User(
        email=email,
        password=generate_password_hash(password)
    )

    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=email)

    return jsonify(
        msg="Usuario registrado correctamente",
        user={"email": email},
        token=token
    ), 201

# =========================
# LOGIN
# =========================
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify(msg="Datos incompletos"), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify(msg="Usuario o contraseña incorrectos"), 401

    token = create_access_token(identity=email)

    return jsonify(
        msg="Login exitoso",
        user={"email": email},
        token=token
    ), 200

# =========================
# IMÁGENES
# =========================
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify(msg="No se envió archivo"), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify(msg="Archivo vacío"), 400

    if not allowed_file(file.filename):
        return jsonify(msg="Formato no permitido"), 400

    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    return jsonify(success=True, filename=filename), 200

@app.route("/images", methods=["GET"])
def list_images():
    return jsonify(os.listdir(app.config["UPLOAD_FOLDER"]))

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# =========================
# ROOT
# =========================
@app.route("/")
def home():
    return jsonify(message="Backend funcionando correctamente")

# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True)
