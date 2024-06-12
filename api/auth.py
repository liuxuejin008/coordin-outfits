import json

from urllib.parse import quote_plus, urlencode
from os import environ as env
from flask import  redirect, render_template, session, url_for, Blueprint

from services.UserService import UserServices

auth_bp = Blueprint('auth', __name__)


from api import oauth

@auth_bp.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("auth.callback", _scheme='https',_external=True)
    )


@auth_bp.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    user_info = token['userinfo']
    email = user_info['email']
    nickname = user_info['nickname']
    user = UserServices.get_user(email)
    if user is None:
        UserServices.add_user(nickname, email, status=0, grade=0, credits=100)
    else:
        print("已经注册了")
    return redirect("/main.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("logout", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )


@auth_bp.route("/home")
def home():
    return render_template("home.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))
