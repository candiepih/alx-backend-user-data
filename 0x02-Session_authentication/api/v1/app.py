#!/usr/bin/env python3
"""
Route module for the API
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

auth_type = getenv('AUTH_TYPE')
if auth_type:
    if auth_type == 'basic_auth':
        from api.v1.auth.basic_auth import BasicAuth
        auth = BasicAuth()
    elif auth_type == 'session_auth':
        from api.v1.auth.session_auth import SessionAuth
        auth = SessionAuth()
    elif auth_type == 'session_exp_auth':
        from api.v1.auth.session_exp_auth import SessionExpAuth
        auth = SessionExpAuth()
    elif auth_type == 'session_db_auth':
        from api.v1.auth.session_db_auth import SessionDBAuth
        auth = SessionDBAuth()
    else:
        from api.v1.auth.auth import Auth
        auth = Auth()


@app.before_request
def before_request():
    """
    Before request handle to check if the
    request is authorized
    """
    if auth:
        excluded_paths = ['/api/v1/status/',
                          '/api/v1/unauthorized/',
                          '/api/v1/forbidden/',
                          '/api/v1/auth_session/login/']
        if auth.require_auth(request.path, excluded_paths):
            if not auth.authorization_header(request) and \
                    not auth.session_cookie(request):
                abort(401)
            current_user = auth.current_user(request)
            if not current_user:
                abort(403)
            request.current_user = current_user


@app.errorhandler(404)
def not_found(error) -> tuple:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> tuple:
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> tuple:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
