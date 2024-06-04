from flask import Flask, jsonify
import os

from api.index import index_bp
from api.users import users_bp

app = Flask(__name__,
                static_url_path='/',  # 配置静态文件的访问 url 前缀)
                static_folder='static',  # 配置静态文件的文件夹
                template_folder='templates'  # 配置模板文件的文件夹
                )

# 注册蓝本
app.register_blueprint(index_bp)
app.register_blueprint(users_bp)
@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})


@app.route('/aa')
def aa():
    return jsonify({"Chaa Chqq": "Welcome to your Flask app 🚅"})




if __name__ == '__main__':

    app.config['upload'] = './upload'
    # Load the views
    from api import index

    app.config['JSON_AS_ASCII'] = False

    # Load the config file
    app.config.from_object('config')
    app.run(debug=True, host="192.168.14.122",port=os.getenv("PORT", default=5000))