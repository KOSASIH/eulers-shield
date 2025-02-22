# api/models.py

class User:
    users_db = {}  # Simulated database

    def __init__(self, user_id, attributes):
        self.user_id = user_id
        self.attributes = attributes
        User.users_db[user_id] = self

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "attributes": self.attributes
        }

    @classmethod
    def get_user(cls, user_id):
        return cls.users_db.get(user_id)

class Post:
    posts_db = {}  # Simulated database

    def __init__(self, post_id, user_id, title, content):
        self.post_id = post_id
        self.user_id = user_id
        self.title = title
        self.content = content
        Post.posts_db[post_id] = self

    def to_dict(self):
        return {
            "post_id": self.post_id,
            "user_id": self.user_id,
            "title": self.title,
            "content": self.content
        }
