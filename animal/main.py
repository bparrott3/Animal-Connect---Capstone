from urllib.parse import quote_plus
from google.cloud import datastore
from flask import Flask, request
from flask import redirect, render_template, session, url_for
from six.moves.urllib.parse import urlencode
from authlib.integrations.flask_client import OAuth


from db_conn import get_db_connection



import owners
import constants
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
def index():
    return render_template("index.html")


@app.route('/flash')
def flash():
    return render_template("flash.html")



@app.route('/users')
def users():
    access = get_access()
    
    if access.lower() == "admin":
        return render_template("users.html")
    else:
        return redirect("https://final-project-407620.wl.r.appspot.com/flash")
    
    



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
        return redirect("https://final-project-407620.wl.r.appspot.com/users")
    
    return (str(res.status_code))
    
  

@app.route('/member-flash')
def member_flash():
    return render_template("member_flash.html")


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
        return redirect("https://final-project-407620.wl.r.appspot.com")
    
    return (str(res.status_code))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + DOMAIN + "/v2/logout?"
        + urlencode(
            {
                "returnTo": "https://final-project-407620.wl.r.appspot.com",
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

@app.route('/access', methods=["GET"])
def get_access():
    user_obj = session.get('user')
    try:
        owner_id = user_obj["userinfo"]["sub"]
        query = client.query(kind=constants.owners)
        results = list(query.fetch())
        
        for e in results:
            if str(e["owner_id"]) == str(owner_id):
                return  e["access"]
    except:
        return ""
    




# for animal profiles html
@app.route('/pets')
def pets():
    conn = get_db_connection()  # Get database connection
    cursor = conn.cursor(dictionary=True)  # Use dictionary cursor to directly get results as dictionaries
    
    query = "SELECT * FROM Animal_Profiles"
    cursor.execute(query)
    profiles = cursor.fetchall()  # Fetch all rows from the query result

    sid = None
    try:
        owner_id = get_owner_id()
        shelter = owners.get_owner(owner_id)
        sid = int(shelter["shelter_id"])
    except:
        sid = ""

    cursor.close()
    conn.close()

    return render_template('animal_profiles.html', profiles=profiles, shelter=shelter, sid=sid)





@app.route('/shelter/id', methods=["GET"])
def get_shelter_id():
    user_obj = session.get('user')
    try:
        owner_id = user_obj["userinfo"]["sub"]

        query = client.query(kind=constants.owners)
        results = list(query.fetch())

        for e in results:
            if str(e["owner_id"]) == str(owner_id):
                return  str(e["shelter_id"])
    except:
        return ""
    


def get_owner_id():
    user_obj = session.get('user')
    try:
        owner_id = user_obj["userinfo"]["sub"]

        return owner_id

    except:
        return ""


@app.route('/shelter')
def shelter():
    access = get_access()
    
    if access.lower() == "member":
        # You can now use shelter_id to fetch data specific to this shelter from your database
        # For example:
        conn = get_db_connection()
        
        
        shelter_id = get_shelter_id()

        owner_id = get_owner_id()
        owner_info = owners.get_owner(owner_id)
        
        # Assuming conn is your MySQL connection object and shelter_id is defined
        cursor = conn.cursor(dictionary=True)  # Use dictionary=True to get results as dictionaries
        
        query = 'SELECT * FROM Animal_Profiles WHERE shelter_id = %s'
        cursor.execute(query, (shelter_id,))
        # Fetch all results
        pet_profiles = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('shelter.html', owner_info=owner_info, pet_profiles=pet_profiles)
    else:
        return redirect("https://final-project-407620.wl.r.appspot.com/member-flash")
    




@app.route('/new-profile')
def new_profile():
    access = get_access()
    
    if access.lower() == "member":
        return render_template('add_profile.html')
    else:
        return redirect("https://final-project-407620.wl.r.appspot.com/member-flash")
    

# for adding a new animal profile
@app.route('/profiles/new', methods=['POST'])
def add_profile():
    # Get form data
    try:
        shelter_id = request.form['shelter_id']
        animal_type = request.form['type']
        breed = request.form['breed']
        disposition = request.form.getlist('disposition')  # Assuming disposition is a list of checkboxes
        availability = request.form['availability']
        description = request.form['description']
        image_url = request.form['image']
        
        # Convert disposition list to a string if needed
        disposition_str = ', '.join(disposition)

        # Connect to the database
        with get_db_connection() as conn:
            with conn.cursor() as cursor:

                # SQL Insert Query
                insert_query = '''
                    INSERT INTO Animal_Profiles (shelter_id, type, breed, disposition, availability, description, image)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                '''
                cursor.execute(insert_query, (shelter_id, animal_type, breed, disposition_str, availability, description, image_url))
                    
                # Commit the transaction
                conn.commit()

                # Close the connection
                cursor.close()
                conn.close()
        
            return redirect("https://final-project-407620.wl.r.appspot.com/shelter")
        
    except Exception as e:
        # Handle the exception (e.g., log the error)
        return f"An error occurred: {str(e)}", 500  # Return a 500 Internal Server Error response






if __name__ == '__main__':
    app.debug = True
    app.run()