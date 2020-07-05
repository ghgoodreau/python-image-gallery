from . import db
from .user import User
from .user_dao import UserDAO


class PostgresUserDAO(UserDAO):
    def __init__(self):
        pass

# DAO version of get Users
    def get_users(self):
        result = []
        cursor = db.execute("select username, password, full_name from users")
        for t in cursor.fetchall():
            result.append(User(t[0], t[1], t[2]))
        return result

# DAO version of get User
    def get_user_by_name(self, username):
        cursor = db.execute("select username, password, full_name from users where username=%s", (username,))
        row = cursor.fetchone()
        if row is not None:
            return User(row[0], row[1], row[2])
        else:
            return None

# DAO version of get Image
    def get_images_by_name(self, username):
        result = []
        cursor = db.execute("select img_name from s3_imgs where username=%s;", (username,))
        for t in cursor.fetchall():
           result.append(t[0])
        return result
