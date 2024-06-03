from flask import Flask

# Initialize the app

app = Flask(__name__,
            static_url_path='/',  # 配置静态文件的访问 url 前缀)
            static_folder='assets',  # 配置静态文件的文件夹
            template_folder='templates'  # 配置模板文件的文件夹
            )

app.config['upload']='./upload'
# Load the views
from api import index

# Load the config file
app.config.from_object('config')
