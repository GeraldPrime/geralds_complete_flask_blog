def get_admin_by_id(cursor, admin_id):
    query = "SELECT * FROM admin WHERE id = %s"
    cursor.execute(query, (admin_id,))
    return cursor.fetchone()


#ORR
def get_admin(cursor):
    query = "SELECT * FROM admin LIMIT 1"
    cursor.execute(query)
    return cursor.fetchone()




def get_all_admins(cursor, descending=False):
    query = "SELECT * FROM admin"
    if descending:
        query += " ORDER BY id DESC"
    cursor.execute(query)
    return cursor.fetchall()


def get_user_by_id(cursor, user_id):
    query = "SELECT * FROM admin WHERE id = %s"
    cursor.execute(query, (user_id,))
    return cursor.fetchone()



# Example usage:
# class Admin:
#     def __init__(self, full_name, email, web_url, name, about, specialty, password, profile_picture):
#         self.full_name = full_name
#         self.email = email
#         self.web_url = web_url
#         self.name = name
#         self.about = about
#         self.specialty = specialty
#         self.password = password
#         self.profile_pictue = profile_picture

# def get_admin(cursor):
#     query = "SELECT * FROM admin LIMIT 1"
#     cursor.execute(query)
#     admin_data = cursor.fetchone()
#     if admin_data:
#         full_name = admin_data['full_name']
#         email = admin_data['email']
#         web_url = admin_data['web_url']
#         name = admin_data['name']
#         about = admin_data['about']
#         specialty = admin_data['specialty']
#         password = admin_data['password']
#         profile_picture = admin_data['profile_picture']
#         return Admin(full_name, email, web_url, name, about, specialty, password, profile_picture)
#     else:
#         return None
