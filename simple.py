from tensorflow import keras
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report
import numpy as np
import cv2
from sklearn.ensemble import RandomForestClassifier

# Load the dataset 
(x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()

# Obtain size of train and test datasets
x_train.shape,x_test.shape

# Normalize the images 
x_train = x_train/255.0 
x_test = x_test/255.0

# Reshape train set into a 2D array for sklearn 
# from (50,000, 32,32,3) 4D to (50,000, 3072) a 2D array 
nsamples, nx, ny, nrgb = x_train.shape 
x_train2 = x_train.reshape((nsamples, nx*ny*nrgb)) #nx*ny*nrgb -> 32*32*3 THE DIMS of img

# Reshape the test set into 2D array 
nsamples, nx, ny, nrgb = x_test.shape 
x_test2 = x_test.reshape((nsamples, nx*ny*nrgb)) #nx*ny*nrgb -> 32*32*3 THE DIMS of img

# Convert labels to 1D array
y_train = y_train.ravel()
y_test = y_test.ravel()

# Random Foreset Classifier 
model = RandomForestClassifier() 

# train the model 
model.fit(x_train2, y_train) # passing in the reshaped training data 

# Predict the test set
y_pred = model.predict(x_test2)

# Calculate accuracy
print("Accuracy:", accuracy_score(y_pred, y_test))

# Print classification report
print("Classification Report:")
print(classification_report(y_pred, y_test))

# Print confusion matrix
print("Confusion Matrix:")
print(confusion_matrix(y_pred, y_test))