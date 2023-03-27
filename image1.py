import streamlit as st
import streamlit.components.v1 as stc
# File Processing Pkgs
import pandas as pd
from PIL import Image 

import os
import json
import hashlib
from io import StringIO

def signup():
    st.write("Create a new account\n")
    username = st.text_input("New_Username")
    password = st.text_input("New_Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if st.button("Signup"):
        if password == confirm_password:
            with open("users.json", "r") as f:
                users = json.load(f)

            if username in users:
                st.error("Username already exists")
            else:
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                users[username] = password_hash
                with open("users.json", "w") as f:
                    json.dump(users, f)
                os.makedirs(f"user_data/{username}")
                st.success("Account created!")
                st.info("Go to Login Menu to login")
        else:
            st.error("Passwords do not match")  
                   
                     
def login():
    st.write("Login to your account\n")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        with open("users.json", "r") as f:
            users = json.load(f)

        if username in users:
            # Hash the user-provided password using SHA-256
            password_hash = hashlib.sha256(password.encode()).hexdigest()

            if users[username] == password_hash:
                st.success("Logged in!")
                st.write(f"Welcome, {username}!")
                # Store the original URL as a query parameter
                st.experimental_set_query_params(Login=True, username=username, original_url=st.experimental_get_query_params().get("original_url", [""])[0])  
            else:
                st.error("Invalid password")
        else:
            st.error("Invalid username")
     
    return None
                   

def upload(username):
    # Display the file upload widget
    image_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    # Check if the user has uploaded an image
    if image_file is not None:
        # Load the image using PIL
        image = Image.open(image_file)

        # Get the width and height of the image
        width, height = image.size

        # Display the original image
        st.image(image, caption="Original Image")

        # Get the user's cropping coordinates
        x = st.slider("Select the starting X coordinate", 0, width, 0)
        y = st.slider("Select the starting Y coordinate", 0, height, 0)
        crop_width = st.slider("Select the crop width", 0, width-x, width)
        crop_height = st.slider("Select the crop height", 0, height-y, height)

        # Crop the image using PIL
        cropped_image = image.crop((x, y, x+crop_width, y+crop_height))

        # Display the cropped image
        st.image(cropped_image, caption="Cropped Image")
        
        if st.button('Save Cropped Image'):
            # Define a file path to save the cropped image
            save_path = f"user_data/{username}"
            os.makedirs(save_path, exist_ok=True) # create the folder if it doesn't exist
            file_name = image_file.name.split('.')[0] # get the file name without extension
            cropped_image.save(f"{save_path}/{file_name}_cropped.png", 'PNG') # save the cropped image with the original name + _cropped.png
            st.success('Cropped Image saved successfully to {}'.format(save_path))


def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo
  
def main():
    st.sidebar.image(add_logo(logo_path=r"C:\Users\SusheelaMagadum\OneDrive - ZapCom Solutions Pvt. ltd\Desktop\zplogo1.png", width=160, height=60))
    # Define menu options
    menu = ["Login", "Signup"]

    # Check if user is logged in
    if "Login" not in st.experimental_get_query_params():
        # If user is not logged in, show login menu option
        choice = st.sidebar.selectbox("Select an option", menu)
        
        if choice == "Login":
            login()
        else:
            signup()
    else:
        # If user is logged in, clear sidebar and show upload menu option
        username = st.experimental_get_query_params()["username"][0]
        st.sidebar.empty()
        st.sidebar.selectbox("Select an option", ["upload"])
        upload(username)

        # Logout button
        if st.sidebar.button("Logout"):
            # Redirect the user back to the original URL path
            st.experimental_set_query_params(params={})



if __name__ == "__main__":
    main()
    
