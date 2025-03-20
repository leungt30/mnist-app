from flask import Flask, render_template, request, jsonify
from PIL import Image
from io import BytesIO
import numpy as np
import tensorflow as tf
from tensorflow.keras import backend
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask_cors import CORS  
from tensorflow import keras
import os

app = Flask(__name__)
CORS(app)

#used to run the python lambda layers
keras.config.enable_unsafe_deserialization()
def absolute_activation(x):
    return backend.abs(x)

CNNModel = load_model('models/RevampedCNN.keras', compile=False, custom_objects={"absolute_activation": absolute_activation})

ConfiguredPort = os.getenv('ConfiguredPort')

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print("POST REQUEST")
        if 'file' not in request.files:
            return 'No file uploaded', 400
        file = request.files['file']
        if file.filename == '':
            return 'No file selected', 400
        if file:
            try:
                print("opening img")
                #open image using PIL
                input_image = Image.open(file.stream)
                
                print("preprocessing")
                #preprocess image
                img_array = preprocessImage(input_image)
                
                #predict on img and inverse
                print("predicting")
                output_pred = CNNModel.predict(img_array)

                print("classifying from predictions")
                predicted_class = np.argmax(output_pred, axis=-1).item()
                print(output_pred)
                predicted_prob = float(output_pred[0][predicted_class])
                
                #can possibly add only output on confidence > threshold

                print(f"Predicted class: {predicted_class}, confidence: {predicted_prob}")
                return jsonify({"class": int(predicted_class), "confidence": predicted_prob})
   
            except Exception as e:
                print(f"Error processing image: {str(e)}")
                return jsonify({"error": str(e)}), 500
    
    return render_template('index.html', port=ConfiguredPort)

def preprocessImage(theImage):
    #grayscale + resize
    theImage = theImage.convert("L")
    theImage = theImage.resize((28,28))
    
    arr = image.img_to_array(theImage)
    #normalize
    arr = np.expand_dims(arr, axis=0)  # Add batch dimension (1, 28, 28)
    arr = arr / 255.0

    return arr

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5100)

