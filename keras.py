import pickle 
import os
import numpy as np 
import matplotlib.pyplot as plt 

import tensorflow as tf 
from keras.api.applications import MobileNetV2
from keras.api.utils import load_img, img_to_array  # Updated for image preprocessing
from keras.api.preprocessing import image
from keras.api.applications.mobilenet_v2 import preprocess_input, decode_predictions
from PIL import Image

# Define the path to the CIFAR-10 batch directory
base_dir = os.path.dirname(os.path.abspath(__file__))  # Path to the directory containing main.py
cifar_dir = os.path.join(base_dir, '../cifar-10-batches-py')

# Access a specific batch file
batch_file = os.path.join(cifar_dir, 'data_batch_1')

# Function to unpickle the batch file
def unpickle(file):
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict

#Load the batch 
batch_data = unpickle(batch_file)

# Acess the data and labels 
images = batch_data[b'data']
labels = batch_data[b'labels']

# Select an image 
image_index = 4
image_flat = images[image_index] 
label = labels[image_index] 

# Reshape image back into (32,32,3) format 
image_reshaped = np.dstack((
    image_flat[:1024].reshape(32,32), # Red channel 
    image_flat[1024:2048].reshape(32,32), # Green Channel 
    image_flat[2048:].reshape(32,32) # Blue channel 
))


# resize the image to 224x224 (required input size for MobileNetV2)
image_resized = np.array(Image.fromarray(image_reshaped.astype('uint8')).resize((224, 224)))

# Preprocess the image
x = img_to_array(image_resized) 
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)

# Load pre-trained MobileNetV2 Model 
model = MobileNetV2(weights='imagenet')

# Predict the image class 
pred = model.predict(x) 
print('Predicted:', decode_predictions(pred, top=3)[0])



# Display the image
plt.imshow(image_reshaped)
plt.title(f'Label: {label}')
plt.axis('off') 
plt.show()