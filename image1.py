import streamlit as st
import streamlit.components.v1 as stc

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
                st.experimental_set_query_params(Login=True, username=username, original_url=st.experimental_get_query_params().get("original_url", [""])[0])  
            else:
                st.error("Invalid password")
        else:
            st.error("Invalid username")
     
    return None
                   

def upload(username):
    image_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

   
    if image_file is not None:
     
        image = Image.open(image_file)

        width, height = image.size

        # Display the original image
        st.image(image, caption="Original Image")

        x = st.slider("Select the starting X coordinate", 0, width, 0)
        y = st.slider("Select the starting Y coordinate", 0, height, 0)
        crop_width = st.slider("Select the crop width", 0, width-x, width)
        crop_height = st.slider("Select the crop height", 0, height-y, height)

        cropped_image = image.crop((x, y, x+crop_width, y+crop_height))

        st.image(cropped_image, caption="Cropped Image")
        
        if st.button('Save Cropped Image'):
            save_path = f"user_data/{username}"
            os.makedirs(save_path, exist_ok=True) 
            file_name = image_file.name.split('.')[0] 
            cropped_image.save(f"{save_path}/{file_name}_cropped.png", 'PNG') 
            st.success('Cropped Image saved successfully to {}'.format(save_path))


def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo
  
def main():
    st.sidebar.image(add_logo(logo_path=r"C:\Users\SusheelaMagadum\OneDrive - ZapCom Solutions Pvt. ltd\Desktop\zplogo1.png", width=160, height=60))
    menu = ["Login", "Signup"]

    if "Login" not in st.experimental_get_query_params():
        choice = st.sidebar.selectbox("Select an option", menu)
        
        if choice == "Login":
            login()
        else:
            signup()
    else:
        username = st.experimental_get_query_params()["username"][0]
        st.sidebar.empty()
        st.sidebar.selectbox("Select an option", ["upload"])
        upload(username)
        
        if st.sidebar.button("Logout"):
            st.experimental_set_query_params(params={})



if __name__ == "__main__":
    main()
    
