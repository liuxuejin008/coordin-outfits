import time

from api.ext import db
from api.models import User


class UserServices:
    @staticmethod
    def get_user(email):
        if not email:
            print("错误：邮箱地址不能为空。")
            return None
        return User.query.filter_by(email=email).first()

    @staticmethod
    def add_user(username, email, status=0, grade=0, credits=100):
        new_user = User(
            username=username,
            email=email,
            status=status,
            grade=grade,
            credits=credits,
            last_update_time=int(time.time()),  # 假设使用当前时间戳
            create_time=int(time.time())
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def update_user(user_id, **kwargs):
        user = UserServices.get_user_by_id(user_id)
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            user.last_update_time = int(time.time())  # 更新更新时间
            db.session.commit()
            return user
        return None

    @staticmethod
    def update_credits(user_id, token):
        user = UserServices.get_user_by_id(user_id)
        if user:
            user.credits = user.credits - token
            user.last_update_time = int(time.time())  # 更新更新时间
            db.session.commit()
            return user
        return None

