from mysql.connector import connect
from .variables import DB_HOST, DB_NAME, DB_PASSWORD,DB_PORT,DB_USER

def get_connection():
  try:
    db = connect (
      host=DB_HOST,
      port=DB_PORT,
      user=DB_USER,
      password=DB_PASSWORD,
      database=DB_NAME
    )

    if db.is_connected(): 
      print("DATABASE CONNECTED")

    cursor = db.cursor(dictionary=True, buffered=True)
    return db, cursor

  except Exception as e:
    print("DATABASE ERROR:", str(e))



def create_admin_table():
  db = get_connection()

  # TERMINATES THE FUNCTION IF THERE'S NO CONNECTION
  if not db:
      return

  connection, cursor = db

  sql = """CREATE TABLE IF NOT EXISTS admin (
      id INT PRIMARY KEY AUTO_INCREMENT,
      name VARCHAR(50) NOT NULL,
      email VARCHAR(70) NOT NULL,
      password VARCHAR(255) NOT NULL,
      profile_picture VARCHAR(255) NULL,
      about TEXT NULL,
      specialty VARCHAR(70) NULL,
      full_name VARCHAR(100) NULL,
      web_url VARCHAR(225) NULL
  )"""

  cursor.execute(sql)
  connection.commit()

  print("(USERS) TABLE CREATED!")
  connection.close()


def create_article_table():
    db = get_connection()

    # TERMINATES THE FUNCTION IF THERE'S NO CONNECTION
    if not db:
        return

    connection, cursor = db

    sql = """CREATE TABLE IF NOT EXISTS article (
        id INT PRIMARY KEY AUTO_INCREMENT,
        title VARCHAR(255) NOT NULL,
        image VARCHAR(255) NOT NULL,
        category INT NOT NULL,
        content TEXT NOT NULL,
        author VARCHAR(100) NOT NULL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP() 
    )"""

    cursor.execute(sql)
    connection.commit()

    print("(POSTS) TABLE CREATED!")
    connection.close()


def create_category_table():
    db = get_connection()

    # TERMINATES THE FUNCTION IF THERE'S NO CONNECTION
    if not db:
        return

    connection, cursor = db

    sql = """CREATE TABLE IF NOT EXISTS category (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(50) NOT NULL
    )"""

    cursor.execute(sql)
    connection.commit()

    print("(EXAMPLE) TABLE CREATED!")

    if connection:
        connection.close()


def create_comment_table():
    db = get_connection()

    # TERMINATES THE FUNCTION IF THERE'S NO CONNECTION
    if not db:
        return

    connection, cursor = db

    sql = """CREATE TABLE IF NOT EXISTS comment (
        id INT PRIMARY KEY AUTO_INCREMENT,
        user_id INT NOT NULL,
        user_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
        article_id INT NOT NULL,
        message VARCHAR(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP() ,
        user_image VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL
    )"""

    cursor.execute(sql)
    connection.commit()

    print("(COMMENT) TABLE CREATED!")

    if connection:
        connection.close()


def create_user_table():
    db = get_connection()

    # TERMINATES THE FUNCTION IF THERE'S NO CONNECTION
    if not db:
        return

    connection, cursor = db

    sql = """CREATE TABLE IF NOT EXISTS user (
        id INT PRIMARY KEY AUTO_INCREMENT,
        username VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
        email VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
        password VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL
    )"""

    cursor.execute(sql)
    connection.commit()

    print("(USERS_CREDENTIALS) TABLE CREATED!")

    if connection:
        connection.close()
