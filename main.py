from flask import  render_template
import os

from api import get_app

print('-----------------------------------init2----------------------------')
app = get_app()

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    print("------------------------启动服务器2222222----------------------")
    app.run(debug=True, port=os.getenv("PORT", default=3000))