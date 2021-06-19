import time
from datetime import datetime
from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash


class User(db.Document):
    username = db.StringField(required=True, unique=True, min_length=4)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True, min_length=8)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode("utf8")

    def check_password(self, password):
        return check_password_hash(self.password, password)

    created_at = db.DateTimeField(default=datetime.utcnow)

    is_admin = db.BooleanField(default=False)


class Category(db.Document):
    name = db.StringField(required=True, unique=True)


class Comments(db.Document):
    body = db.StringField(required=True)
    created = db.DateTimeField(require=True)
    user = db.ReferenceField("User")


class Poems(db.Document):
    author = db.ReferenceField("User", require=True)
    title = db.StringField(required=True, max_value=80)
    body = db.StringField(required=True)
    category = db.ReferenceField("Category", dbref="True")
    comments = db.ListField(
        db.ReferenceField("Comments", reverse_delete_rule=db.CASCADE)
    )


# Comments.register_delete_rule(Poems, "comments", db.CASCADE)
