from flask import Flask, request, send_file
from PIL import Image
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['OUTPUT_FOLDER'] = 'static/outputs'

def generate_output_filename(input_filename):
    base_name, ext = os.path.splitext(input_filename)
    return f"bw_{base_name}{ext}"

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    
    input_filename = file.filename
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], input_filename)
    output_filename = generate_output_filename(input_filename)
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

    file.save(input_path)
    
    image = Image.open(input_path).convert('L')  # Convert to black and white
    image.save(output_path)
    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
