from flask import Flask, jsonify
import os


from api import app



@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})


@app.route('/aa')
def aa():
    return jsonify({"Chaa Chqq": "Welcome to your Flask app 🚅"})




if __name__ == '__main__':
    app.run(debug=True, host="192.168.14.122",port=os.getenv("PORT", default=5000))