from .category import get_one_category

# THIS SEEMS TO BE WORKING FINE ON MY SYSTEM, IT WASN'T SHOWING THAT MUILT ...BLAH ...BLAH ERROR 
def get_all_articles(cursor, descending=False):
  query = """
    SELECT A.*, C.name as cat_name 
    FROM article as A
    INNER JOIN category as C
    ON A.category = C.id
    """
  
  if descending: query = """
    SELECT A.*, C.name as cat_name 
    FROM article as A
    INNER JOIN category as C
    ON A.category = C.id 
    ORDER BY id DESC
  """
  cursor.execute(query)
  return cursor.fetchall()

# HERE'S IS ANOTHER ALTERNATIVE, JUST INCASE THIS ONE DOESN'T WORK OUT.
def get_all_articles_alt(cursor, descending=False):
  query = "SELECT * FROM article"
  
  if descending: query = "SELECT * FROM article ORDER BY id DESC"
  cursor.execute(query)
  
  # GET ALL ARTICLES 
  articles = cursor.fetchall()

  data = []
  for article in articles:
    # GET THE CATEGORY
    category = get_one_category(cursor, article.get("category"))
    # ADD A NEW PROPERTY TO THE ARTICLE
    article['cat_name'] = category.get("name")
    data.append(article)
  
  return data




def get_one_article(cursor, id):
  #to get just id
  #query = "SELECT * FROM article WHERE id = %s"
  #to get the id and category name
  query = """
    SELECT article.*, category.name AS cat_name
    FROM article
    JOIN category ON article.category = category.id
    WHERE article.id = %s
    """
  cursor.execute(query, [id])
  return cursor.fetchone()


def get_articles(cursor, descending=False, random_order=False, num_articles=None):
    query = """
        SELECT A.*, C.name as cat_name 
        FROM article as A
        INNER JOIN category as C
        ON A.category = C.id
    """

    if descending:
        query += " ORDER BY id DESC"

    if random_order:
        query += " ORDER BY RAND()"

    if num_articles:
        query += f" LIMIT {num_articles}"

    cursor.execute(query)
    return cursor.fetchall()
  


# Modified function to get the latest article
def get_latest_article(cursor):
    query = """
        SELECT A.*, C.name as cat_name 
        FROM article as A
        INNER JOIN category as C
        ON A.category = C.id
        ORDER BY A.date DESC
        LIMIT 1
    """
    cursor.execute(query)
    return cursor.fetchone()


def get_articles_by_category_name(cursor, category_name):
    query = """
        SELECT * FROM article
        WHERE category = (SELECT id FROM category WHERE name = %s)
    """
    cursor.execute(query, [category_name])

    return cursor.fetchall()


def get_articles_by_category_id(cursor, category_id):
    query = """
        SELECT * FROM article
        WHERE category = (SELECT id FROM category WHERE id = %s)
    """
    cursor.execute(query, [category_id])
    return cursor.fetchall()

def get_random_articles_by_category(cursor, category_name, descending=False, random_order=False, num_articles=None):
    query = """
        SELECT A.*, C.name as cat_name 
        FROM article as A
        INNER JOIN category as C
        ON A.category = C.id
        WHERE C.name = %s
    """

    if descending:
        query += " ORDER BY id DESC"

    if random_order:
        query += " ORDER BY RAND()"

    if num_articles:
        query += f" LIMIT {num_articles}"

    cursor.execute(query, [category_name])
    return cursor.fetchall()

#serch function


# def search_articles(cursor, search_query):
#     query = """
#         SELECT A.*, C.name AS cat_name
#         FROM article AS A
#         INNER JOIN category as C ON A.category = C.id
#         WHERE A.title LIKE %s OR A.content LIKE %s OR C.name LIKE %s
#         ORDER BY date DESC
#     """
#     # Use '%' to match any substring
#     search_pattern = f"%{search_query}%"

#     cursor.execute(query, [search_pattern, search_pattern, search_pattern])

#     # Fetch all results
#     search_results = cursor.fetchall()

#     return search_results


def search_articles(cursor, search_query, page=1, results_per_page=10):
    # Calculate the starting index based on the page number and results per page
    start_index = (page - 1) * results_per_page

    query = """
        SELECT A.*, C.name AS cat_name
        FROM article AS A
        INNER JOIN category as C ON A.category = C.id
        WHERE A.title LIKE %s OR A.content LIKE %s OR C.name LIKE %s
        ORDER BY date DESC
        LIMIT %s OFFSET %s
    """

    # Use '%' to match any substring
    search_pattern = f"%{search_query}%"

    cursor.execute(query, [search_pattern, search_pattern,
                   search_pattern, results_per_page, start_index])

    # Fetch all results
    search_results = cursor.fetchall()

    return search_results


# def search_articles(cursor, search_query, page=1, results_per_page=10):
#     # Calculate the starting index based on the page number and results per page
#     start_index = (page - 1) * results_per_page

#     query = """
#         SELECT A.*, C.name AS cat_name
#         FROM article AS A
#         INNER JOIN category as C ON A.category = C.id
#         WHERE A.title LIKE %s OR A.content LIKE %s OR C.name LIKE %s
#         ORDER BY date DESC
#         LIMIT %s OFFSET %s
#     """

#     count_query = """
#         SELECT COUNT(*) 
#         FROM article AS A
#         INNER JOIN category as C ON A.category = C.id
#         WHERE A.title LIKE %s OR A.content LIKE %s OR C.name LIKE %s
#     """

#     # Use '%' to match any substring
#     search_pattern = f"%{search_query}%"

#     cursor.execute(query, [search_pattern, search_pattern,
#                    search_pattern, results_per_page, start_index])

#     # Fetch all results
#     search_results = cursor.fetchall()

#     # Get the total count of results without LIMIT and OFFSET
#     cursor.execute(count_query, [search_pattern,
#                    search_pattern, search_pattern])
#     total_results = cursor.fetchone()[0]

#     return search_results, total_results
