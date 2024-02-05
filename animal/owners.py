from google.cloud import datastore
from flask import Blueprint, request, make_response
from flask import jsonify

from jose import jwt
from six.moves.urllib.request import urlopen

import requests
import json
import constants


bp = Blueprint('owners', __name__, url_prefix='/owners')
client = datastore.Client()

# dev-zc1xnd0zpdccf4v1 is my Auth account
CLIENT_ID = 'QTDHOj6bruGVKQ0dVl6pXnzA91V4FQQV'
CLIENT_SECRET = 'w0tPzc02h5gGbhdkI8H5CNzHzZHkHvkLpoRM9FfRau-YVAK03FHLuQoWYU_n5YnN'
DOMAIN = 'dev-zc1xnd0zpdccf4v1.us.auth0.com'

ALGORITHMS = ["RS256"]

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

@bp.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

# Verify the JWT in the request's Authorization header
def verify_jwt(request):
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        bear_space = auth_header[0:7]

        if bear_space != "Bearer ":
            raise AuthError({"code": "no Bearer",
                            "description":
                                "Bearer keyword is missing"}, 401)
        else:
            token = auth_header.split()[1]
    else:
        raise AuthError({"code": "no auth header",
                            "description":
                                "Authorization header is missing"}, 401)
    
    jsonurl = urlopen("https://"+ DOMAIN +"/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.JWTError:
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Invalid header. "
                            "Use an RS256 signed JWT Access Token"}, 401)
    if unverified_header["alg"] == "HS256":
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Invalid header. "
                            "Use an RS256 signed JWT Access Token"}, 401)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=CLIENT_ID,
                issuer="https://"+ DOMAIN+"/"
            )
        except jwt.ExpiredSignatureError:
            raise AuthError({"code": "token_expired",
                            "description": "token is expired"}, 401)
        except jwt.JWTClaimsError:
            raise AuthError({"code": "invalid_claims",
                            "description":
                                "incorrect claims,"
                                " please check the audience and issuer"}, 401)
        except Exception:
            raise AuthError({"code": "invalid_header",
                            "description":
                                "Unable to parse authentication"
                                " token."}, 401)

        return payload
    else:
        raise AuthError({"code": "no_rsa_key",
                            "description":
                                "No RSA key in JWKS"}, 401)


# CREATE an owner: 3 attributes
# 1) jwt-sub id = owner's unique id
# 2) name
# 3) email
# 4) list of boats
# 5) self link
# return 201 if created
# return 401 covered by verify_jwt()
# auto-gen id not displayed, name does not have to be unique
# assum body is valid

@bp.route('', methods=['GET','POST'])
def add_owner_get_owners():
    if not ('application/json' in request.accept_mimetypes):
            msg = "{'Error': 'Client's acceptable MIME type is not supported by the endpoint'}"
            return (msg, 406)
    
    if request.method == 'POST':
        payload = verify_jwt(request)
        jwt_sub = payload["sub"]

        owner_info = _has_owner(jwt_sub)
        if owner_info:
            return ({'exisiting': owner_info}, 200)

        else:
            if not ('application/json' in request.content_type):
                msg = "{'Error': 'Unsupported MIME type was sent, please send JSON type only'}"
                return (msg, 415)
        
            new_owner = datastore.entity.Entity(key=client.key(constants.owners))
            new_owner.update({"owner_id": jwt_sub,
                              "name": payload["nickname"], 
                              "email": payload["email"],
                              "boats": []
                             })
            new_owner["self"] = request.base_url + "/" + jwt_sub
            client.put(new_owner)

            res = make_response(new_owner)
            res.mimetype = 'application/json'
            res.status_code = 201
            return res

    elif  request.method == 'GET':
        query = client.query(kind=constants.owners)
        results = list(query.fetch())

        res = make_response(results)
        res.mimetype = 'application/json'
        res.status_code = 200
        return res

    else:
        return ('Method not recognized', 405)
    

# NOT REQUIRED, ONLY FOR DEVELOPER
# Only deleting owners off the database, not from Auth0
# @bp.route('/<owner_id>', methods=['DELETE'])
# def delete_owner(owner_id):
#     if  request.method == 'DELETE':
#         payload = verify_jwt(request)
#         jwt_sub = payload["sub"]

#         if str(jwt_sub) != str(owner_id):
#             msg = {'Error': 'JWT is valid but it does not match with this owner_id'}
#             return (msg, 403)

#         try:
#             owner_key = client.key(constants.boats, int(owner_id))
#             client.delete(owner_key)
#             return ("", 204)
#         except:
#             msg = {'Error': 'No owner with this owner_id exists'}
#             return (msg, 403)

#     else:
#         return ('Method not recognized', 405)



def _has_owner(owner_id):
    query = client.query(kind=constants.owners)
    results = list(query.fetch())

    for e in results:
        if str(e["owner_id"]) == str(owner_id):
            return e
        
    return None




###################### EXTRA STUFF #######################

# Decode the JWT supplied in the Authorization header
# @bp.route('/decode', methods=['GET'])
# def jwt_decode():
#     payload = verify_jwt(request)
#     return payload["sub"]

# Generate a JWT from the Auth0 domain and return it
# Request: JSON body with 2 properties with "username" and "password"
#       of a user registered with this Auth0 domain
# Response: JSON with the JWT as the value of the property id_token
@bp.route('/jwt', methods=['POST'])
def jwt_get():
    if not ('application/json' in request.accept_mimetypes):
            msg = "{'Error': 'Client's acceptable MIME type is not supported by the endpoint'}"
            return (msg, 406)
    if not ('application/json' in request.content_type):
            msg = "{'Error': 'Unsupported MIME type was sent, please send JSON type only'}"
            return (msg, 415)
    
    if request.method == 'POST':
        content = request.get_json()
        username = content["username"]
        password = content["password"]
        body = {'grant_type':'password',
                'username':username,
                'password':password,
                'client_id':CLIENT_ID,
                'client_secret':CLIENT_SECRET
            }
        headers = { 'content-type': 'application/json' }
        url = 'https://' + DOMAIN + '/oauth/token'
        r = requests.post(url, json=body, headers=headers)

        return r.text, 200, {'Content-Type':'application/json'}
    else:
        return ('Method not recognized', 405)
