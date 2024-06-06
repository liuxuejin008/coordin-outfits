
from flask import Flask, jsonify, render_template
import os

from api.auth import auth_bp
from api.index import index_bp
from api.users import users_bp

from api import  app

# 注册蓝本
app.register_blueprint(index_bp)
app.register_blueprint(users_bp)
app.register_blueprint(auth_bp)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/aa')
def aa():
    return jsonify({"Chaa Chqq": "Welcome to your Flask app 🚅"})




if __name__ == '__main__':

    app.config['upload'] = './upload'
    # Load the views
    from api import index, app

    app.config['JSON_AS_ASCII'] = False

    # Load the config file
    app.config.from_object('config')
    app.run(debug=True, port=os.getenv("PORT", default=3000))