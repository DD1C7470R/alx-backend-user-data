#!/usr/bin/env python3
"""
Main app file
"""
import os
from os import getenv
from flask import Flask, jsonify, abort, request, make_response, redirect
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def index():
    """index handler.
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def all_users():
    """index handler.
    """
    email = request.form.get("email")
    if email is None:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get("password")
    if password is None:
        return jsonify({"error": "password missing"}), 400

    try:
        user = AUTH.register_user(email, password)
        return jsonify({
            "email": email,
            "message": "user created"
        })

    except Exception as e:
        return jsonify({"message": "email already registered"})


@app.route('/sessions', methods=['POST'])
def user_login():
    """implement a login function.
    """
    email = request.form.get("email")
    if email is None:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get("password")
    if password is None:
        return jsonify({"error": "password missing"}), 400

    try:
        is_valid_user = AUTH.valid_login(email, password)
        if not is_valid_user:
            abort(401)

        session_id = AUTH.create_session(email)
        resp = make_response(jsonify({
            "email": email,
            "message": "logged in"
        }))
        resp.set_cookie("session_id", session_id)
        return resp

    except Exception as e:
        raise e


@app.route('/sessions', methods=['DELETE'])
def user_logout():
    """ If the user exists destroy the
    session and redirect the user to GET /
    """
    try:
        session_id = request.cookies.get('session_id')
        user = AUTH.get_user_from_session_id(session_id)
        if user is None:
            abort(403)
        AUTH.destroy_session(user.id)
        return redirect('/')
    except Exception as e:
        raise e


@app.route('/reset_password', methods=['POST'])
def request_reset_password():
    """ If the user exists destroy the
    session and redirect the user to GET /
    """
    try:
        email = request.form.get('email')
        if email is None or not isinstance(email, str):
            abort(403)
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token})
    except Exception as e:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def reset_password():
    """ If the user exists destroy the
    session and redirect the user to GET /
    """
    try:
        email = request.form.get('email')
        if email is None or not isinstance(email, str):
            abort(403)
        reset_token = request.form.get('reset_token')
        if reset_token is None or not isinstance(reset_token, str):
            abort(403)
        new_password = request.form.get('new_password')
        if new_password is None or not isinstance(new_password, str):
            abort(403)

        reset_token = AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})

    except Exception as e:
        return abort(403)


@app.route('/profile', methods=['GET'])
def user_profile():
    """ returns user profile
    """
    try:
        session_id = request.cookies.get('session_id')
        user = AUTH.get_user_from_session_id(session_id)
        if user is None:
            abort(403)
        return jsonify({"email": user.email})

    except Exception as e:
        raise e


@app.errorhandler(403)
def forbidden(error) -> str:
    """Forbidden handler.
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
