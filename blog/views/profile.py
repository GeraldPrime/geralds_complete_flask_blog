from flask import Blueprint, render_template, request, flash, redirect, current_app
from ..utils.decorators import autheticated_admin
from ..config.database import get_connection
from ..store.profile import get_admin
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from ..utils.helpers import sub_words, profile_picture_upload
import os
import logging
import random
import string
import time



profile = Blueprint("profile", __name__)
db = get_connection()


# HANDLE VIEWS PROFILE PAGE
@profile.get("/")
@autheticated_admin
def profile_page():
  if not db:
    flash("Error connecting to db", "danger") 
    return redirect("/owner")
  
  conn, cursor = db
  admin = get_admin(cursor)

  
  # admin['profile_picture'] = os.path.join('static', 'profile_uploads', admin['profile_picture'])  # Construct the full file path
  


  return render_template("admin/pages-profile.html", admin=admin)
 


# Handle update profile
@profile.route('/edit', methods=['POST'])
@autheticated_admin
def update_profile():
    form = request.form
    image = request.files.get("image")
    prev_image = form.get("prev-image")

   
        
    if secure_filename(image.filename):
        data = profile_picture_upload(image)
        image_name = data.get("filename")

        # DELETE PREV IMAGE
        prev_image_path = os.path.join(current_app.config['PROFILE_UPLOAD_PATH'], form.get(
            "prev-image"))  # GET THE FILE PATH
        if os.path.exists(prev_image_path): # CHECK IF FILE EXISTS
           os.remove(prev_image_path) # DELETE FILE
    
    

    # upload_folder = 'static/profile_uploads/'
    # if secure_filename(image.filename):
    #     # Handle new profile picture upload
    #     data = profile_picture_upload(image)
    #     image_name = data.get("filename")

    #     # Delete previous profile picture
    #     prev_image_path = os.path.join(upload_folder, prev_image)
    #     if os.path.exists(prev_image_path):
    #         os.remove(prev_image_path)
    #     else:
    #     # Use the previous profile picture if no new image is uploaded
    #         image_name = prev_image

    # Get form values
    full_name = form.get("FullName")
    email = form.get("Email")
    web_url = form.get("web-url")
    name = form.get("Username")
    password = form.get("Password")
    about = form.get("AboutMe")
    specialty = form.get("Specialty")
    hashed_password = generate_password_hash(password)

    # Establish database connection
    try:
        db, cursor = get_connection()

        # Update user profile in the database
        query = """
            UPDATE admin 
            SET full_name = %s, 
                email = %s, 
                web_url = %s, 
                name = %s, 
                about = %s, 
                password = %s,
                specialty = %s,
                profile_picture = %s
        """

        cursor.execute(query, [full_name, email, web_url, name,about, hashed_password, specialty, image_name])
        

        db.commit()

        # Check if the update was successful
        if cursor.rowcount > 0:
            flash("Profile updated successfully!", "success")
        else:
            flash("Failed to update profile", "danger")

    except Exception as e:
        logging.error("Error occurred while updating profile", exc_info=True)
        flash("Error occurred while updating profile", "danger")
    

    return redirect('/owner/profile')


