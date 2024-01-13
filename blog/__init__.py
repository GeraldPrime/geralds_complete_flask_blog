from flask import Flask, render_template
from .config.variables import SECRET_KEY
import os

# GETS THE FOLDER (ABSOLUTE) NAME FOR THE `__init__.py` -> something.../blog/
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def create_app():
  app = Flask(__name__) 

  # CONFIGS
  app.config["SECRET_KEY"] = SECRET_KEY
  # JOINS THE BASE DIRECTORY WITH /static/uploads -> something.../blog/static/uploads/
  app.config["BLOG_UPLOAD_PATH"] = os.path.join(BASE_DIR, "static/uploads/") 
  app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024 # 2MB
  app.config['PROFILE_UPLOAD_PATH'] = os.path.join(BASE_DIR, "static/profile_uploads/") 


  # BLUEPRINT
  from .views.admin_auth import admin
  app.register_blueprint(admin, url_prefix="/owner")

  from .views.category import category
  app.register_blueprint(category, url_prefix="/owner/category")

  from .views.article import article
  app.register_blueprint(article, url_prefix="/owner/article")

  from .views.profile import profile
  app.register_blueprint(profile, url_prefix="/owner/profile")
 
  from .views.user_auth import user
  app.register_blueprint(user, url_prefix="/user")


  # ERROR 404
  @app.errorhandler(404)
  def page_not_found(error):
    print("404 ERROR:", str(error))
    return render_template("error-404.html")
  

  # ERROR 500
  # @app.errorhandler(Exception)
  # def server_error(error):
  #   print("500 ERROR:", str(error))
  #   return render_template("error-500.html")
  

  return app