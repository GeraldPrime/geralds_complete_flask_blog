# from flask import Blueprint, render_template, request, flash, redirect
# from ..utils.decorators import autheticated_admin
# from ..config.database import get_connection
# from ..store.category import get_all_categories, get_one_category
# from ..store.profile import get_admin


# user = Blueprint("user", __name__)
# db = get_connection()


# @user.get("/")
# @autheticated_admin
# def user_page():
#   if not db:
#     flash("Error connecting to db", "danger")
#     return redirect("/owner")

#   _, cursor = db
#   editing = None
#   categories = get_all_categories(cursor, True)
#   admin = get_admin(cursor)

#   if request.args.get("cat_id"):
#     editing = get_one_category(cursor, id=request.args.get("cat_id"))

#   return render_template("user/home_page.html", admin=admin, categories=categories, editing=editing)
