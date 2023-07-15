from db import db


class UserModel(db.Model):

    __tablename__ = "user"

    id = db.Column(db.Interger, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)