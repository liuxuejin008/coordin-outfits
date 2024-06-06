
# Initialize the app
from flask import Flask
from os import environ as env
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


#static_folder 和 template_folder都是执行文件路径，如果app初始化在根目录下，这个/static没有问题，但是现在
#api目录下，这个时候要往上一层路径
app = Flask(__name__,
                static_url_path='/',  # 配置静态文件的访问 url 前缀)
                static_folder='../static',  # 配置静态文件的文件夹
                template_folder='../templates'  # 配置模板文件的文件夹
                )
app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)
print(env.get("AUTH0_DOMAIN"))
oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

