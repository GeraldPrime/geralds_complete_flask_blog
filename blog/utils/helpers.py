from flask import current_app
from werkzeug.utils import secure_filename
import os
from datetime import datetime

def sub_words(text:str, length):
    words = text.split(" ")
    if length > len(words): return text
    return " ".join(words[0:length])


def article_file_upload(image):
    data = {
        "filename": None,
        "error":None
    }

    if not secure_filename(image.filename): 
        data['error'] = "No file selected!"
        return data

    # CHECK IMAGE TYPE
    allowed_types = ["image/png", "image/jpeg", "image/jpg"]
    if not image.mimetype in allowed_types:
       data['error'] = "file (type) not allowed"
       return data

    # UPLOAD IMAGE
    filename = f'{datetime.now().timestamp()}-{secure_filename(image.filename)}'
    image.save(os.path.join(
        current_app.config["BLOG_UPLOAD_PATH"],
        filename
    ))

    data['filename'] = filename
    return data


# def profile_picture_upload(image):
#     data = {
#         "filename": None,
#         "error":None
#     }

#     if not secure_filename(image.filename): 
#         data['error'] = "No file selected!"
#         return data

#     # CHECK IMAGE TYPE
#     allowed_types = ["image/png", "image/jpeg", "image/jpg"]
#     if not image.mimetype in allowed_types:
#        data['error'] = "file (type) not allowed"
#        return data

#     # UPLOAD IMAGE
#     filename = f'{datetime.now().timestamp()}-{secure_filename(image.filename)}'
#     image.save(os.path.join(
#         current_app.config["PROFILE_PICTURE_UPLOAD_PATH"],
#         filename
#     ))

#     data['filename'] = filename
#     return data


def profile_picture_upload(image):
    if not secure_filename(image.filename):
        return {"filename": None, "error": "No file selected!"}

    allowed_types = ["image/png", "image/jpeg", "image/jpg"]
    if not image.mimetype in allowed_types:
        return {"filename": None, "error": "File type not allowed!"}

    filename = f'{datetime.now().timestamp()}-{secure_filename(image.filename)}'
    image.save(os.path.join(
        current_app.config["PROFILE_UPLOAD_PATH"], filename))

    return {"filename": filename, "error": None}






