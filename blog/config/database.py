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