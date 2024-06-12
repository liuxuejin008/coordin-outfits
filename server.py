"""Python Flask WebApp Auth0 integration example
"""
import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for

from api import oauth, app, db
from services.UserService import UserServices

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)


# Controllers API
@app.route("/")
def home():
    return render_template(
        "home.html",
        session=session.get("user"),
        pretty=json.dumps(session.get("user"), indent=4),
    )


@app.route("/callback", methods=["GET", "POST"])
def callback():
    print("===============callback=============")
    token = oauth.auth0.authorize_access_token()
    print("===================userinfo=================")
    print(token['userinfo'])

    user_info = token['userinfo']

    email = user_info['email']
    nickname = user_info['nickname']
    user = UserServices.get_user(email)
    if user is None:
        UserServices.add_user(nickname, email, status=0, grade=0, credits=100)
    else:
        print("已经注册了")
    print("===================userinfo=================")
    session["user"] = token
    session["userName"] = "tom"
    return redirect("/")


@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://"
        + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.route('/get_session')
def get_session():
    username = session.get('username')
    if username is None:
        username="notSessionUserNanme"
    return 'get session username {}'.format(username)


@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    return render_template('signin.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=env.get("PORT", 3000))