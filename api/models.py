from api.ext import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    status = db.Column(db.Integer,default=0)
    grade = db.Column(db.Integer, default=0)
    credits = db.Column(db.Integer, default=100)
    last_update_time = db.Column(db.BigInteger, nullable=False)
    create_time = db.Column(db.BigInteger, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

