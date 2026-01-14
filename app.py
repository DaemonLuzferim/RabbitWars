from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

# =========================
# Configuración
# =========================
app = Flask(__name__)
CORS(app)  # Permitir acceso desde cualquier frontend

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# =========================
# Rutas
# =========================

# Subir imagen
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'success': True, 'filename': filename}), 200
    else:
        return jsonify({'error': 'File type not allowed'}), 400

# Listar imágenes subidas
@app.route('/images', methods=['GET'])
def list_images():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify(files)

# Servir imágenes
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Ruta principal (opcional para probar)
@app.route('/')
def home():
    return jsonify({'message': 'Backend funcionando'})

# =========================
# Ejecutar
# =========================
if __name__ == '__main__':
    app.run(debug=True)
