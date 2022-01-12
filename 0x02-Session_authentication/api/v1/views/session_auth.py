#!/usr/bin/env python3
"""
Contains session auth paths
"""
import os
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.user import User


@app_views.route('/auth_session/login',
                 methods=['POST'], strict_slashes=False)
def login():
    """
    Login the user in
    """
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user "
                                 "found for this email"}), 404
    found_user = users[0]
    if not found_user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(found_user.id)
    user_data = jsonify(found_user.to_json())
    user_data.set_cookie(os.getenv('SESSION_NAME'), session_id)
    return user_data, 200


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    """
    Logout the user

    Returns:
        json: {} if successful
    """
    from api.v1.app import auth
    del_session = auth.destroy_session(request)
    if not del_session:
        abort(404)
    return jsonify({}), 200
