from flask import Blueprint, render_template, flash, redirect, abort, request, current_app
from ..utils.decorators import autheticated_admin
from ..utils.helpers import sub_words, article_file_upload
from ..config.database import get_connection
from ..store.category import get_all_categories
from ..store.article import get_all_articles, get_one_article, get_all_articles_alt
from werkzeug.utils import secure_filename 
from datetime import datetime
import os
from ..store.profile import get_admin

article = Blueprint("article", __name__)
db = get_connection()


# HANDLE VIEWS ARTICLES PAGE
@article.get("/")
@autheticated_admin
def articles_page():
  if not db:
    return abort(500, "Error connecting to db")
  
  conn, cursor = db
  # articles = get_all_articles_alt(cursor)
  articles = get_all_articles(cursor)
  admin = get_admin(cursor)
  
  return render_template("admin/view-article.html",admin=admin, articles=articles, sub_words=sub_words)


# HANDLE ADD ARTICLES PAGE
@article.get("/add")
@autheticated_admin
def add_article_page():
  if not db:
    return abort(500, "Error connecting to db")
  
  conn, cursor = db
  categories = get_all_categories(cursor)
  admin = get_admin(cursor)
  
  
  return render_template("admin/add-article.html",admin=admin, categories=categories)


# HANDLE EDIT ARTICLE PAGE
@article.get("/edit/<id>")
@autheticated_admin
def edit_article_page(id):
  if not db:
    return abort(500, "Error connecting to db")
  
  conn, cursor = db
  categories = get_all_categories(cursor)
  article = get_one_article(cursor, id)
  admin = get_admin(cursor)
  
  
  return render_template("admin/edit-article.html", admin=admin, categories=categories, article=article)


# HANDLE DELETE ARTICLE PAGE
@article.get("/delete/<id>")
@autheticated_admin
def delete_article(id):
  if not db:
    return abort(500, "Error connecting to db")
  
  conn, cursor = db
  query = "DELETE FROM article WHERE id = %s"
  cursor.execute(query, [id])
  conn.commit()


  if not cursor.rowcount: 
    flash("Failed to delete article!", "danger")
    return redirect("/owner/article/")
  
  flash("Article deleted!", "success")
  return redirect("/owner/article/")


# HANDLE CREATE NEW ARTICLE
@article.post("/create")
@autheticated_admin
def create_article():
  form = request.form
  image = request.files.get("image")

  data = article_file_upload(image)

  if data.get('error'):
    flash(data.get('error'), "danger")
    return redirect("/owner/article/add")
  
  filename = data.get("filename")
  title = form.get("title")
  category = form.get("category")
  author = form.get("author")
  content = form.get("content")

  if not db:
    return abort(500, "Error connecting to db")
  
  conn, cursor = db

  # INSERT TO DATABASE
  query = "INSERT INTO article (title, image, category, content, author) VALUES (%s, %s, %s, %s, %s)"
  cursor.execute(query, [title, filename, category, content, author])
  conn.commit()

  if not cursor.rowcount: 
    flash("Failed to add article", "danger")
    return redirect("/owner/article/add")
  
  flash("Article added!", "success")
  return redirect("/owner/article/")


# HANDLE UPDATE ARTICLE
@article.post("/update")
@autheticated_admin
def update_article():
  form = request.form
  image = request.files.get("image")
  image_name = form.get("prev-image")

  if secure_filename(image.filename):
    data = article_file_upload(image)
    image_name = data.get("filename")

    # DELETE PREV IMAGE
    prev_image_path = os.path.join(current_app.config['BLOG_UPLOAD_PATH'], form.get("prev-image")) # GET THE FILE PATH
    if os.path.exists(prev_image_path): # CHECK IF FILE EXISTS
      os.remove(prev_image_path) # DELETE FILE
    

  # GET FORM VALUES
  title = form.get("title")
  category = form.get("category")
  author = form.get("author")
  content = form.get("content")
  article_id = form.get("id")

  # CHECK CONNECTION
  if not db:
    return abort(500, "Error connecting to db")
  
  conn, cursor = db

  # UPDATE TABLE
  query = """
    UPDATE article 
    SET title = %s, 
      image = %s, 
      category = %s, 
      content = %s, 
      author = %s 
    WHERE id = %s
  """
  cursor.execute(query, [title, image_name, category, content, author, article_id])
  conn.commit()

  # CHECK IF INSERTED
  if not cursor.rowcount: 
    flash("Failed to update article", "danger")
    return redirect(f"/owner/article/edit/{article_id}")
  
  flash("Article updated!", "success")
  return redirect("/owner/article/")
