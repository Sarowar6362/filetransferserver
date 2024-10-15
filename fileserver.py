from flask import Flask, request, send_from_directory, jsonify
import os
from flask_cors import CORS

app = Flask(__name__) 
CORS(app)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  


app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB 

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Save the file in the uploads folder
    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    # Respond with a success message
    response = jsonify({'message': f'File {filename} uploaded successfully!'})
    print(response.get_data(as_text=True))  
    return response


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    if os.path.exists(filepath):
        return send_from_directory(UPLOAD_FOLDER, filename)
    else:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
