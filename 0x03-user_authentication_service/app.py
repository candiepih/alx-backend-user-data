#!/usr/bin/env python3
"""
Setup of a basic Flask app
"""
from flask import Flask, jsonify, request, abort, redirect, url_for, Response
from auth import Auth
from typing import Union

app = Flask(__name__)
Auth = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def home() -> str:
    """
    Home route
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user() -> Union[str, tuple]:
    """
    Register user route
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        Auth.register_user(email, password)
        return jsonify({"email": "{}".format(email),
                        "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
    Login user route. Creates a session_id cookie for the user
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not Auth.valid_login(email, password):
        abort(401)
    session_id = Auth.create_session(email)
    res_data = {"email": "{}".format(email), "message": "logged in"}
    res = jsonify(res_data)
    res.set_cookie('session_id', session_id)
    return res


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout_user() -> Response:
    """
    Logout user route
    """
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    user = Auth.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    setattr(user, 'session_id', None)
    return redirect(url_for('home'))


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> Union[str, tuple]:
    """
    Profile route
    """
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    user = Auth.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    return jsonify({"email": "{}".format(user.email)}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def reset_password() -> tuple:
    """
    Reset password route
    """
    email = request.form.get('email')
    try:
        token = Auth.get_reset_password_token(email)
        return jsonify({"email": "{}".format(email),
                        "reset_token": "{}".format(token)}), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def reset_password_with_token() -> tuple:
    """
    Reset password with token route
    """
    email = request.form.get('email')
    new_password = request.form.get('new_password')
    reset_token = request.form.get('reset_token')

    try:
        user_reset_token = Auth.get_reset_password_token(email)
        if user_reset_token != reset_token:
            abort(403)
        Auth.update_password(reset_token, new_password)
        return jsonify({"email": "{}".format(email),
                        "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
