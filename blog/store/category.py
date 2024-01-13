def get_all_categories(cursor, descending=False):
  query = "SELECT * FROM category"
  if descending: query = "SELECT * FROM category ORDER BY id DESC"
  cursor.execute(query)
  return cursor.fetchall()
  



def get_one_category(cursor, id):
  query = "SELECT * FROM category WHERE id = %s"
  cursor.execute(query, [id])
  return cursor.fetchone()
  

def get_category_article_counts(cursor):
    #to display categories with articles
    query = """
        SELECT C.name as category_name, COUNT(A.id) as article_count
        FROM article as A
        INNER JOIN category as C ON A.category = C.id
        GROUP BY C.name
    """

    #OR 
    # to display all categories regardless of if they have articles or not
    # query = """
    #     SELECT C.name as category_name, COUNT(A.id) as article_count
    #     FROM category as C
    #     LEFT JOIN article as A ON A.category = C.id
    #     GROUP BY C.name
    # """
    cursor.execute(query)
    return cursor.fetchall()


def get_all_users(cursor, descending=False):
  query = "SELECT * FROM user"
  if descending: query = "SELECT * FROM user ORDER BY id DESC"
  cursor.execute(query)
  return cursor.fetchall()