from flask import  render_template
import os

from api.auth import auth_bp
from api.index import index_bp
from api.users import users_bp

from api import app
from api import db


# 注册蓝本
app.register_blueprint(index_bp)
app.register_blueprint(users_bp)
app.register_blueprint(auth_bp)

with app.app_context():
    print("-------------------------创建数据库表----------------------")
    db.create_all()



@app.route('/')
def index():
    print("------------------------index2222222----------------------")
    return render_template('index.html')


if __name__ == '__main__':
    print("------------------------启动服务器2222222----------------------")

    app.run(debug=True, port=os.getenv("PORT", default=3000))