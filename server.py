from flask import Flask, request, jsonify
from PIL import Image
import pytesseract as tess
tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)

@app.route("/imgt", methods=["POST"])
def process_image():
    file = request.files['image']
    img = Image.open(file.stream)
    text = tess.image_to_string(img, lang='deu')
    return jsonify(text)
    


if __name__ == "__main__":
    app.run(debug=True)