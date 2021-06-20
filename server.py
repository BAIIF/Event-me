from flask import Flask, request, jsonify
from PIL import Image
import pytesseract as tess
tess.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'

app = Flask(__name__)

@app.route("/imgt", methods=["POST", "GET"])
def process_image():
    file = request.files['image']
    img = Image.open(file.stream)
    text = tess.image_to_string(img, lang='deu')
    return print(text)
    
@app.route('/')
def index():
    return "Hello World" 

if __name__ == "__main__":
    app.run(debug=True)