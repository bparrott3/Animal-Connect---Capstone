from urllib.parse import quote_plus
from google.cloud import datastore
from flask import Flask
from flask import redirect, render_template, session, url_for
from six.moves.urllib.parse import urlencode
from authlib.integrations.flask_client import OAuth

import owners


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
    if user_obj:
        user_jwt = user_obj["id_token"]
        return render_template("home.html", user_obj=user_obj, user_jwt=user_jwt)
    
    return render_template("home.html", user_obj=user_obj)


@app.route('/jwt', methods=["GET"])
def jwt():
    user_obj = session.get('user')
    if user_obj:
        user_jwt = user_obj["id_token"]
        return user_jwt
    
    return ""


@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


# after authentication
@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("https://65bbfab1c325a826144f3c8d--kaleidoscopic-cannoli-6cc07f.netlify.app")


# after logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + DOMAIN + "/v2/logout?"
        + urlencode(
            {
                "returnTo": "https://65bbfab1c325a826144f3c8d--kaleidoscopic-cannoli-6cc07f.netlify.app",
                "client_id": CLIENT_ID
            }, 
            quote_via=quote_plus
        )
    )



if __name__ == '__main__':
    # app.run(host='127.0.0.1', port=8080, debug=True)
    app.debug = True
    app.run()