from flask import Blueprint, render_template, request, flash, redirect, session, url_for
from ..utils.decorators import autheticated_admin, authenticated_user
from ..config.database import get_connection
from ..store.category import get_all_categories, get_one_category, get_category_article_counts
from ..store.profile import get_admin
from werkzeug.security import generate_password_hash, check_password_hash
from ..store.article import get_all_articles, get_one_article, get_all_articles_alt, get_articles, get_latest_article, get_articles_by_category_name,  get_random_articles_by_category, get_articles_by_category_id, search_articles
from ..utils.helpers import sub_words, article_file_upload
from flask_paginate import Pagination, get_page_args


user = Blueprint("user", __name__)
db = get_connection()


@user.get("/register")
def user_register():
    return render_template("user/user_register.html")


@user.post("/create")
def handle_register_user():
    form = request.form

    # GET THE FORM FIELDS
    username = form.get("username")
    email = form.get("email")
    password = form.get("password")
    hashed_password = generate_password_hash(password)

    if not db:
        flash("Error connecting to db", "danger")
        return redirect("/user/register")

    conn, cursor = db
    query = "INSERT INTO user(username, email, password) VALUES (%s, %s, %s)"
    cursor.execute(query, [username, email, hashed_password])
    conn.commit()

    if not cursor.rowcount:
        flash("Failed to register user", "danger")
        return redirect("/user/register")

    flash("Registration successful!", "success")
    return redirect("/user")


# HANDLE USER LOGIN
@user.post("/login")
def handle_login_user():
    form = request.form

    # FROM FIELDS
    email = form.get("email")
    password = form.get("password")

    if not db:
        flash("Error connecting to db", "danger")
        return redirect("/user/register")

    conn, cursor = db

    # GET THE USER
    query = "SELECT * FROM user WHERE email = %s"
    cursor.execute(query, [email])

    user = cursor.fetchone()
    print(user)

    stored_password = user.get("password")
    print("Stored Password:", stored_password)
    print("Password Match:", check_password_hash(stored_password, password))

    if not user:
        flash("User does not exist", "danger")
        return redirect("/user/register")

  
    # VERIFY THE PASSWORD
    if not check_password_hash(user.get("password"), password):
        flash("Incorrect credentials", "danger")
        return redirect("/user/register")
    


    # CREATE USER LOGIN SESSION
    session["USER_LOGIN"] = user.get("email")
    session["USERNAME"] = user.get("username")
    session["USER_ID"] = user.get("id")

    flash("Login successful!", "success")
    return redirect("/user")


# HANDLE USER LOGOUT
@user.get("/logout")
def logout_admin():
  
  session.pop("USER_LOGIN", None)

  return redirect("/user")


@user.get("/")
def user_home_page():
    if not db:
        flash("Error connecting to db", "danger")
        return redirect("/user/register")

    _, cursor = db
    editing = None
    # get the articles
    # categories = get_all_categories(cursor, True)

    # get the admin
    admin = get_admin(cursor)

    # get all the articles
    articles = get_all_articles(cursor)

    #get random number of articles
    sports_random_articles = get_random_articles_by_category(cursor, "sports", random_order=True, num_articles=3) #for the first sports section
    lifestyle_random_articles= get_random_articles_by_category(cursor, "lifestyle", random_order=True, num_articles=4)#for the first lifestyle section

    random_articles = get_articles(cursor, random_order=True, num_articles=10)

    footer_articles = get_articles(cursor, descending=True, random_order=False,num_articles=3)


    #get the last article
    last_article = get_latest_article(cursor)

    #get one article
    one_article = get_one_article(cursor, id=4)

    #get article by category
    article_category = get_articles_by_category_name(cursor, "sports")

    #display category and count
    categories = get_category_article_counts(cursor)

    # Get the search query from the URL parameters
    search_query = request.args.get('query', '')

    # Perform a search in the database for articles matching the query
    search_results = search_articles(cursor, search_query)



    if request.args.get("cat_id"):
        editing = get_one_category(cursor, id=request.args.get("cat_id"))

    return render_template("user/index.html", random_articles=random_articles, lifestyle_random_articles=lifestyle_random_articles, sports_random_articles=sports_random_articles, article_category=article_category, last_article=last_article, one_article=one_article, articles=articles, admin=admin, categories=categories, editing=editing,  sub_words=sub_words, search_query=search_query, search_results=search_results, footer_articles=footer_articles)


# @user.get('/article_single/<int:article_id>')
# def article_detail(article_id):
#     #estalish connection
#     if not db:
#         flash("Error connecting to db", "danger")
#         return redirect("/user/register")

#     _, cursor = db
#     editing = None

#     #get the admin
#     admin= get_admin(cursor)

#     # Retrieve the article details using article_id
#     article = get_one_article(cursor, article_id)

#     categories=get_category_article_counts(cursor)
    

#     #display 5 random articles at the bottom
#     random_articles = get_articles(cursor, random_order=True, num_articles=5)

#      # Get the category name of the current article
#     category_name = article.get('cat_name')

#     # Get more articles in the same category
#     related_articles = get_random_articles_by_category(cursor, category_name, random_order=False, num_articles=3)


#     return render_template('user/article_single.html',sub_words=sub_words, related_articles=related_articles, random_articles=random_articles, admin=admin,  article=article, categories=categories)


@user.get('/article_single/<int:article_id>')
def article_detail(article_id):
    # Establish connection
    if not db:
        flash("Error connecting to db", "danger")
        return redirect("/user/register")

    conn, cursor = db

    # Get the admin
    admin = get_admin(cursor)

    # Retrieve the article details using article_id
    article = get_one_article(cursor, article_id)

    # Get the comments for the current article
    query = "SELECT * FROM comment WHERE article_id = %s"
    cursor.execute(query, (article_id,))
    conn.commit()
    comments = cursor.fetchall()

    categories = get_category_article_counts(cursor)

    # Display 5 random articles at the bottom
    random_articles = get_articles(cursor, random_order=True, num_articles=5)

    footer_articles = get_articles(cursor, descending=True, random_order=False,num_articles=3)

    # Get the category name of the current article
    category_name = article.get('cat_name')

    # Get more articles in the same category
    related_articles = get_random_articles_by_category(
        cursor, category_name, random_order=False, num_articles=3)

    return render_template(
        'user/article_single.html',
        sub_words=sub_words,
        related_articles=related_articles,
        random_articles=random_articles,
        admin=admin,
        article=article,
        comments=comments,
        categories=categories,
        footer_articles=footer_articles
    )




@user.get('/category/<category_name>')
def category_page(category_name):

    if not db:
        flash("Error connecting to db", "danger")
        return redirect("/user/register")

    _, cursor = db

    #get admin
    admin= get_admin(cursor)
    # article_category = get_articles_by_category_name(cursor, category_name)
    article_category = get_random_articles_by_category(cursor, category_name, random_order=False, num_articles=200000000)

    #display article categories and how many articles are there
    categories = get_category_article_counts(cursor)

    #display random articles
    random_articles = get_articles(cursor, random_order=True, num_articles=5)

    footer_articles = get_articles(cursor, descending=True, random_order=False,num_articles=3)

    # article_category=get_articles_by_category_id(cursor, category_id)

    return render_template('user/category_page.html',category_name=category_name, random_articles=random_articles, admin=admin,categories=categories, sub_words=sub_words, article_category=article_category, footer_articles=footer_articles)


@user.get('/contact')
def contact_page():
    if not db:
        flash("Error connecting to db", "danger")
        return redirect("/user/register")

    _, cursor = db

    categories = get_category_article_counts(cursor)
    footer_articles = get_articles(
        cursor, descending=True, random_order=False, num_articles=3)
    # get admin
    admin = get_admin(cursor)
    return render_template('user/contact.html', admin=admin , categories=categories, footer_articles=footer_articles )


# @user.get('/search-results')
# def search_results():
#     if not db:
#         flash("Error connecting to db", "danger")
#         return redirect("/user/register")

#     _, cursor = db

#     admin = get_admin(cursor)

#     categories = get_category_article_counts(cursor)

#     # Get the search query from the URL parameters
#     search_query = request.args.get('query', '')

#     # Perform a search in the database for articles matching the query
#     search_results = search_articles(cursor, search_query)

#     return render_template('user/search_page.html', admin=admin, sub_words=sub_words, search_query=search_query, search_results=search_results,categories=categories)




# @user.get('/search_results')
# def search_results():
#     if not db:
#         flash("Error connecting to db", "danger")
#         return redirect("/user/register")

#     _, cursor = db

#     admin = get_admin(cursor)

#     # Get the search query from the URL parameters
#     search_query = request.args.get('query', '')

#     # Pagination configuration
#     page, per_page, offset = get_page_args(
#         page_parameter='page', per_page_parameter='per_page')
#     per_page = 3  # Set the number of items per page
    

#     search_results = search_articles(cursor, search_query)
#     total_results=len(search_results)

#     # Perform a search in the database for articles matching the query with pagination
#     # search_results, total_results = search_articles(
#     #     cursor, search_query, page=page, results_per_page=per_page)



#     # Pagination
#     pagination = Pagination(page=page, per_page=per_page,
#                             total=total_results, css_framework='bootstrap4')

#     print('search query:', search_query)
#     print(search_results)
#     categories = get_category_article_counts(cursor)

#     return render_template('user/search_page.html', categories=categories, admin=admin, sub_words=sub_words,
#                            search_query=search_query, search_results=search_results, pagination=pagination)

@user.get('/search_results')
def search_results():
    if not db:
        flash("Error connecting to db", "danger")
        return redirect("/user/register")

    _, cursor = db

    admin = get_admin(cursor)

    # Get the search query from the URL parameters
    search_query = request.args.get('query', '')

    # Perform a search in the database for articles matching the query
    search_results = search_articles(cursor, search_query)

    random_articles = get_articles(cursor, random_order=True, num_articles=4) #get random articles

    # Calculate total results without pagination
    total_results = len(search_results)

    # Pagination configuration
    page, per_page, offset = get_page_args(
        page_parameter='page', per_page_parameter='per_page')
    per_page = 3  # Set the number of items per page

    # Perform a search in the database for articles matching the query with pagination
    search_results_paginated = search_articles(
        cursor, search_query, page=page, results_per_page=per_page)

    # Pagination
    pagination = Pagination(page=page, per_page=per_page,
                            total=total_results, css_framework='bootstrap4')
    
    footer_articles = get_articles(
        cursor, descending=True, random_order=False, num_articles=3)
    
    print(pagination)

    print('search query:', search_query)
    print(search_results_paginated)
    categories = get_category_article_counts(cursor)

    return render_template('user/search_page.html', categories=categories, admin=admin, sub_words=sub_words, 
                        search_query=search_query, search_results=search_results_paginated, pagination=pagination, random_articles=random_articles, footer_articles=footer_articles)



# @authenticated_user
# @app.post('/article/<int:article_id>/add_comment')
# def add_comment(article_id):
#     if not db:
#         flash("Error connecting to db", "danger")
#         return redirect("/user/register")

#     user_id = request.form['user_id']  # Replace with actual user_id
#     user_name = request.form['user_name']  # Replace with actual user_name
#     message = request.form['message']

#     cursor = conn.cursor()
#     query = "INSERT INTO comment (user_id, user_name, article_id, message) VALUES (%s, %s, %s, %s)"
#     cursor.execute(query, (user_id, user_name, article_id, message))
#     conn.commit()
    

#     # Redirect to the article page or wherever you want
#     return redirect('/article_single', comments=comments)





@authenticated_user
@user.post('/article/<int:article_id>/add_comment')
def add_comment(article_id):
    user_id = session.get("USER_ID")
    user_name = session.get("USERNAME")
    message = request.form['message']

    if not user_id or not user_name:
        flash("You need to be logged in to add a comment. Please register or log in.", "danger")
        return redirect(url_for('user.user_register'))

    if not db:
        flash("Error connecting to db", "danger")
        return redirect(url_for('user.user_register'))

    conn, cursor = db
    query = "INSERT INTO comment (user_id, user_name, article_id, message, date) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)"
    cursor.execute(query, (user_id, user_name, article_id, message))
    conn.commit()

    # Redirect to the article page or wherever you want
    return redirect(url_for('user.article_detail', article_id=article_id))
