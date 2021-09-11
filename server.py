from flask import Flask, request, jsonify
from PIL import Image
import io, os
from google.cloud import vision
import datefinder




os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r'eventme-318812-c378b2f19c9b.json'
app = Flask(__name__)
date= ""
result = {}


@app.route("/imgt", methods=["POST", "GET"])
def process_image():
    global result
    if request.method == 'POST':
        file = request.files['image']
        img = Image.open(file.stream)
        img = img.save("saved.jpg")

    if os.stat("saved.jpg").st_size > 1000000:
        file_size = os.stat("saved.jpg").st_size  # determine the size of th image in bytes
        quality = 60
        while file_size > 1000000:  # while the image size more then 1 MB
            img = Image.open("saved.jpg")  # open the old image
            img.save("saved.jpg", optimize=True, quality=quality)  # save the new low quality image
            file_size = os.stat("saved.jpg").st_size  # determine the new file size
            quality -= 10  # try with less quality

    client = vision.ImageAnnotatorClient()
    with io.open("saved.jpg", 'rb') as image_file:
       content = image_file.read()
    image = vision.Image(content=content)
        
    response = client.text_detection(image=image)
    text = response.text_annotations[0].description

    dates = datefinder.find_dates(text)
    for n in dates: 
         dates= str(n) 

    date=""
    time=""
    for n in range(0, 10):
        date+=str(dates[n])
   

    for n in range(11,19):
        time+=str(dates[n])


    result.update({ "date": date, "time":time  })

        
      
    return jsonify(result)
    
    
@app.route('/')
def index():
    global result
    return result
    


if __name__ == "__main__":
    app.run(debug=True)

