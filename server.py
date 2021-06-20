from flask import Flask, request, jsonify
from PIL import Image
import pytesseract as tess

app = Flask(__name__)
text = "a"
@app.route("/imgt", methods=["POST", "GET"])


def process_image():
    global text
    if request.method == 'POST':
        file = request.files['image']
        img = Image.open(file.stream)
        text = tess.image_to_string(img, lang='eng')
 
        return jsonify(text)

@app.route('/')
def index():
    global text
    return text
    
    
    


if __name__ == "__main__":
    app.run(debug=True)