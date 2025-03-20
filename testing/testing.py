from tensorflow.keras.models import load_model
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras import backend
import numpy as np
from tensorflow import keras

keras.config.enable_unsafe_deserialization()

# Define the function manually if needed
def absolute_activation(x):
    return backend.abs(x)

model = load_model('models/RevampedCNN.keras', custom_objects= {"absolute_activation": absolute_activation})
img = image.load_img('number_6.png', target_size=(28,28), color_mode='grayscale')
img_array = image.img_to_array(img)  # Convert image to array
img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension (1, 28, 28)

# Normalize the image (if needed)
img_array = img_array / 255.0  # Scale pixel values to [0, 1] range (for MNIST or similar datasets)

predictions = model.predict(img_array)
print(predictions)
predicted_class = np.argmax(predictions, axis=-1)  # This will give the index of the highest probability
print(f"Predicted class: {predicted_class[0]}")
