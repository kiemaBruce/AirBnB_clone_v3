#!/usr/bin/python3
"""Handles all default RESTFul API actions for User objects"""

from api.v1.views import app_views
from datetime import datetime
from flask import abort, jsonify, request
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET', 'POST'])
@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET',
                 'DELETE', 'PUT'])
def users(user_id=None):
    """Defines some RESTFul API actions for User objects"""
    if user_id:
        user_object = storage.get(User, user_id)
    if request.method == 'GET':
        if user_id is None:  # Retrieve all users
            user_objs = storage.all(User).values()
            users_list = [obj.to_dict() for obj in user_objs]
            return jsonify(users_list)
        elif user_object is None:  # No such user exists
            abort(404)
        # Return user with that id
        return jsonify(user_object.to_dict())
    elif request.method == 'DELETE':
        if user_object is None:  # No such user exists
            abort(404)
        # Delete that specific user
        user_object.delete()
        storage.save()
        return jsonify({}), 200
    elif request.method == 'POST':
        # Create new User object
        if request.headers.get('Content-Type') != 'application/json':
            abort(400, 'Not a JSON')
        data_dict = request.get_json()
        if data_dict is None:
            abort(400, 'Not a JSON')
        if 'email' not in data_dict:
            abort(400, 'Missing email')
        if 'password' not in data_dict:
            abort(400, 'Missing password')
        allowed_attrs = ['first_name', 'last_name', 'email', 'password']
        filtered_dict = {
                            key: value
                            for key, value in data_dict.items()
                            if key in allowed_attrs
                            }
        """
        filtered_dict = {}
        for key, value in data_dict.items():
            if key in allowed_attrs:
                filtered_dict[key] = value
        """
        new_user = User(**filtered_dict)
        new_user.save()
        return jsonify(new_user.to_dict()), 201
    elif request.method == 'PUT':
        # Update existing User object
        if user_object is None:
            abort(404)
        if request.headers.get('Content-Type') != 'application/json':
            abort(400, 'Not a JSON')
        data_dict = request.get_json()
        if data_dict is None:
            abort(400, 'Not a JSON')
        forbidden_list = ['id', 'created_at', 'updated_at', 'email']
        allowed_attrs = ['first_name', 'last_name', 'password']
        for key, value in data_dict.items():
            if key not in forbidden_list and key in allowed_attrs:
                setattr(user_object, key, value)
        # change the updated_at attribute
        setattr(user_object, 'updated_at', datetime.utcnow())
        storage.save()
        return jsonify(user_object.to_dict()), 200
