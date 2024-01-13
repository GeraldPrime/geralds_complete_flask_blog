from flask import Blueprint, render_template, request, flash, redirect
from ..utils.decorators import autheticated_admin
from ..config.database import get_connection
from ..store.category import get_all_categories, get_one_category
from ..store.profile import get_admin


category = Blueprint("category", __name__)
db = get_connection()

@category.get("/")
@autheticated_admin
def category_page():
  if not db:
    flash("Error connecting to db", "danger") 
    return redirect("/owner")
  
  _, cursor = db
  editing = None
  categories = get_all_categories(cursor, True)
  admin = get_admin(cursor)
  

  if request.args.get("cat_id"):
    editing = get_one_category(cursor, id=request.args.get("cat_id"))

  

  return render_template("admin/category.html",admin=admin, categories=categories, editing=editing)


@category.post("/create")
@autheticated_admin
def handle_create_category():
  form = request.form

  name = form.get("category")

  if not db:
    flash("Error connecting to db", "danger")
    return redirect("/owner/category")
  
  conn, cursor = db
  query = "INSERT INTO category(name) VALUES (%s)"
  cursor.execute(query, [name])
  conn.commit()

  if not cursor.rowcount:
    flash("Failed to add category", "danger")
    return redirect("/owner/category")
  
  flash("Category added successfully!", "success")
  return redirect("/owner/category")


@category.get("/delete/<id>")
@autheticated_admin
def handle_delete_category(id):
  if not db:
    flash("Error connecting to db", "danger")
    return redirect("/owner/category")
  
  conn, cursor = db
  query = "DELETE FROM category WHERE id = %s"
  cursor.execute(query, [id])
  conn.commit()

  if not cursor.rowcount:
    flash("Failed to delete category", "danger")
    return redirect("/owner/category")
  
  flash("Category deleted successfully!", "success")
  return redirect("/owner/category")


@category.post("/update/<id>")
@autheticated_admin
def handle_update_category(id):
  name = request.form.get("category")
  if not db:
    flash("Error connecting to db", "danger")
    return redirect("/owner/category")
  
  conn, cursor = db
  query = "UPDATE category SET name = %s WHERE id = %s"
  cursor.execute(query, [name, id])
  conn.commit()

  if not cursor.rowcount:
    flash("Failed to update category", "danger")
    return redirect("/owner/category")
  
  flash("Category updated successfully!", "success")
  return redirect("/owner/category")
