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




@bp.route('', methods=['GET'])
def get_owners():
    
    if  request.method == 'GET':
        query = client.query(kind=constants.owners)
        results = list(query.fetch())

        return results, 200


    else:
        return ('Method not recognized', 405)
    


@bp.route('/admin', methods=['POST'])
def add_admin():
    
    if request.method == 'POST':
        payload = verify_jwt(request)
        jwt_sub = payload["sub"]

        owner_info = _has_owner(jwt_sub)
        if owner_info:
            return ({'exisiting': owner_info}, 200)

        else:
            new_owner = datastore.entity.Entity(key=client.key(constants.owners))
            new_owner.update({"owner_id": jwt_sub,
                            "first_name": "",
                            "last_name": "", 
                            "phone": "",
                            "address": "",
                            "email": payload["email"],
                            "access": "admin"
                            })
            new_owner["self"] = request.base_url + "/" + jwt_sub
            client.put(new_owner)

            res = make_response(new_owner)
            res.mimetype = 'application/json'
            res.status_code = 201
            return res

    else:
        return ('Method not recognized', 405)



@bp.route('/member', methods=['POST'])
def add_member():
    
    if request.method == 'POST':
        payload = verify_jwt(request)
        jwt_sub = payload["sub"]

        owner_info = _has_owner(jwt_sub)
        if owner_info:
            return ({'exisiting': owner_info}, 200)

        else:
            new_owner = datastore.entity.Entity(key=client.key(constants.owners))
            new_owner.update({"owner_id": jwt_sub,
                            "first_name": "",
                            "last_name": "", 
                            "phone": "",
                            "address": "",
                            "email": payload["email"],
                            "access": "member"
                            })
            new_owner["self"] = request.base_url + "/" + jwt_sub
            client.put(new_owner)

            res = make_response(new_owner)
            res.mimetype = 'application/json'
            res.status_code = 201
            return res

    else:
        return ('Method not recognized', 405)



@bp.route('/<owner_id>', methods=['GET'])
def get_owner(owner_id):
    if  request.method == 'GET':
        query = client.query(kind=constants.owners)
        results = list(query.fetch())

        for e in results:
            if str(e["owner_id"]) == str(owner_id):
                return (json.dumps(e), 200)

        return ('User not found', 404)
    


@bp.route('/database/<id>', methods=['PATCH'])
def patch_owners(id):
    if request.method == 'PATCH':
        owner_key = client.key(constants.owners, int(id))
        owner = client.get(key=owner_key)
        if not owner:
            return "Owner not found", 404
    
        try:
            content = request.get_json()

            owner.update({"first_name": content["first_name"],
                        "last_name": content["last_name"],
                        "phone": content["phone"],
                        "address": content["address"],
                        "email": content["email"],
                        "access": content["access"]})
            client.put(owner)

            return "", 200
        
        except:
            return "Sorry didn't work"






@bp.route('/access/<owner_id>', methods=['GET'])
def get_access(owner_id):
    if  request.method == 'GET':
        query = client.query(kind=constants.owners)
        results = list(query.fetch())

        for e in results:
            if str(e["owner_id"]) == str(owner_id):
                return e["access"]
            
        return None







def _has_owner(owner_id):
    query = client.query(kind=constants.owners)
    results = list(query.fetch())

    for e in results:
        if str(e["owner_id"]) == str(owner_id):
            return e
        
    return None

