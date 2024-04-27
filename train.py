import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import pandas as pd
import streamlit as st
from PIL import Image

# Load the pre-trained food classification model
model = load_model('model.h5')

# Load the dataset containing food names and calories
dataset = pd.read_csv('food_dataset.csv', encoding='latin1')

# Function to predict the food class
def predict_food(img):
    img = cv2.resize(img, (100, 100))  # Resize the image to match the model's input shape
    img = np.expand_dims(img, axis=0)
    img = img / 255.0  # Normalize the image
    prediction = model.predict(img)
    food_class = np.argmax(prediction)
    return food_class

# Function to get calorie information for the predicted food class
def get_calories(food_class):
    food_name = dataset.loc[food_class, 'Food']
    calories = dataset.loc[food_class, 'Calories']
    return food_name, calories

# Main function to detect food and print calories
def main():
    st.title('Food Detection and Calorie Estimation')
    st.write("Upload an image containing food to detect the food and estimate its calories.")

    # Upload image
    uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        # Convert the file to an opencv image
        file_bytes = np.asarray(bytearray(uploaded_image.read()), dtype=np.uint8)
        opencv_image = cv2.imdecode(file_bytes, 1)
        
        # Display uploaded image
        st.image(opencv_image, channels='BGR', caption='Uploaded Image', use_column_width=True)

        # Predict the food class
        food_class = predict_food(opencv_image)
        
        # Get calorie information for the predicted food class
        food_name, calories = get_calories(food_class)
        
        # Print the results
        st.write("Calories:", calories)

if __name__ == "__main__":
    main()
