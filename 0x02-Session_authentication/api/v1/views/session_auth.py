#!/usr/bin/env python3
"""
Contains session auth paths
"""
import os
from api.v1.views import app_views
from flask import jsonify, request
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
    Login
    """
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    found_user = users[0]
    if not found_user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    print(os.getenv("API_PORT"))
    from api.v1.app import auth
    session_id = auth.create_session(found_user.id)
    user_data = jsonify(found_user.to_dict())
    user_data.set_cookie(os.getenv('SESSION_NAME'), session_id)
    return user_data, 200
