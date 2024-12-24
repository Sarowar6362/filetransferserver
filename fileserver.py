from flask import Flask, request, send_from_directory, jsonify
import os
from flask_cors import CORS

app = Flask(__name__) 
CORS(app)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Save the file in chunks to avoid memory issues
    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    with open(filepath, 'wb') as f:
        for chunk in file.stream:
            f.write(chunk)
    
    # Respond with a success message
    return jsonify({'message': f'File {filename} uploaded successfully!'})

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    if os.path.exists(filepath):
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
    else:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
