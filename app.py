from flask import Flask, request, jsonify
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

import tensorflow as tf
import numpy as np
import cv2
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow requests from frontend

MODEL_PATH = "bovine_model.h5"
DATA_DIR = "data"

model = tf.keras.models.load_model(MODEL_PATH)
class_names = sorted([d for d in os.listdir(os.path.join(DATA_DIR, "cow_breeds")) if os.path.isdir(os.path.join(DATA_DIR, "cow_breeds", d))])
IMAGE_SIZE = 224

def preprocess_image(file_bytes):
    np_arr = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (IMAGE_SIZE, IMAGE_SIZE))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img / 255.0
    return np.expand_dims(img, axis=0)

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'Empty file name'}), 400

    try:
        # Read image and preprocess it
        file_bytes = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (224, 224))
        img = img / 255.0
        image = np.expand_dims(img, axis=0)  # 👈 this defines `image`

        # Predict
        prediction = model.predict(image)
        predicted_class = class_names[np.argmax(prediction)]

        return jsonify({'breed': predicted_class})
    
    except Exception as e:
        print("Prediction error:", e)
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
