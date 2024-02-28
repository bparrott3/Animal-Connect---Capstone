from urllib.parse import quote_plus
from google.cloud import datastore
from flask import Flask
from flask import redirect, render_template, session, url_for
from six.moves.urllib.parse import urlencode
from authlib.integrations.flask_client import OAuth

import owners
import requests

app = Flask(__name__)
app.secret_key = 'SECRET_KEY'
app.register_blueprint(owners.bp)


client = datastore.Client()

CLIENT_ID = 'QTDHOj6bruGVKQ0dVl6pXnzA91V4FQQV'
CLIENT_SECRET = 'w0tPzc02h5gGbhdkI8H5CNzHzZHkHvkLpoRM9FfRau-YVAK03FHLuQoWYU_n5YnN'
DOMAIN = 'dev-zc1xnd0zpdccf4v1.us.auth0.com'


oauth = OAuth(app)
oauth.register(
    'auth0',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    api_base_url="https://" + DOMAIN,
    access_token_url="https://" + DOMAIN + "/oauth/token",
    authorize_url="https://" + DOMAIN + "/authorize",
    client_kwargs={'scope': 'openid profile email'
                  },
    server_metadata_url="https://" + DOMAIN + "/.well-known/openid-configuration"
)




@app.route('/')
def home():
    user_obj = session.get('user')
    
    return render_template("home.html", user_obj=user_obj)


@app.route('/users')
def users():
    user_obj = session.get('user')
    user_id = user_obj["userinfo"]["sub"]
    url = "https://final-project-407620.wl.r.appspot.com/owners/access/" + user_id
    if user_obj:
        res = requests.get(url)
        if res.text == "admin":
            return render_template("users.html")
        else:
            return ("Admin privilege only", 401)
    return ("Admin privilege only", 401)


@app.route('/animal')
def animal():
    return render_template("animal.html")

@app.route('/database')
def database():
    user_obj = session.get('user')
    user_id = user_obj["userinfo"]["sub"]
    url = "https://final-project-407620.wl.r.appspot.com/owners/access/" + user_id
    if user_obj:
        res = requests.get(url)
        if res.text == "admin":
            return render_template("database.html")
            # return redirect("steven's url")
        else:
            return ("Admin privilege only", 401)
    return ("Admin privilege only", 401)

@app.route("/admin-login")
def admin_login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("admin_callback", _external=True)
    )

@app.route("/admin-callback")
def admin_callback():

    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    user_jwt = token["id_token"]

    url = "https://final-project-407620.wl.r.appspot.com/owners/admin"
    headers = {
        'Authorization': 'Bearer ' + user_jwt
    }

    res = requests.post(url, headers=headers)
    

    if res.status_code == 200 or res.status_code == 201:
        return redirect("https://final-project-407620.wl.r.appspot.com/database")
    
    return (str(res.status_code))
    
  



@app.route("/member-login")
def member_login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("member_callback", _external=True)
    )

@app.route("/member-callback")
def member_callback():

    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    user_jwt = token["id_token"]

    url = "https://final-project-407620.wl.r.appspot.com/owners/member"
    headers = {
        'Authorization': 'Bearer ' + user_jwt
    }

    res = requests.post(url, headers=headers)

    if res.status_code == 200 or res.status_code == 201:
        return redirect("https://final-project-407620.wl.r.appspot.com/animal")
    
    return (str(res.status_code))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + DOMAIN + "/v2/logout?"
        + urlencode(
            {
                "returnTo": "https://final-project-407620.wl.r.appspot.com/animal",
                "client_id": CLIENT_ID
            },
            quote_via=quote_plus
        )
    )



@app.route('/jwt', methods=["GET"])
def jwt():
    user_obj = session.get('user')
    if user_obj:
        user_jwt = user_obj["id_token"]
        return user_jwt
    
    return ""








if __name__ == '__main__':
    app.debug = True
    app.run()