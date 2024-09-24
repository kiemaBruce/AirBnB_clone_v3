#!/usr/bin/python3
"""Handles all RESTful API actions for State objects."""

from api.v1.views import app_views
from datetime import datetime
from flask import abort, jsonify, request
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET', 'POST'])
@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET',
                 'DELETE', 'PUT'])
def states(state_id=None):
    state_object = storage.get(State, state_id)
    if request.method == 'GET':
        if state_id is None:
            return_list = []
            states_dict = storage.all(State)
            for value in states_dict.values():
                return_list.append(value.to_dict())
            return jsonify(return_list)
        if state_object is None:
            abort(404)
        return jsonify(state_object.to_dict())
    elif request.method == 'DELETE':
        if state_object is None:
            abort(404)
        state_object.delete()
        storage.save()
        return jsonify({}), 200
    elif request.method == 'POST':
        # we have to create an entirely new object (e.g. auto-generated id)
        data_dict = request.get_json()
        if data_dict is None:
            abort(400, 'Not a JSON')
        if 'name' not in data_dict:
            abort(400, 'Missing name')
        new_state = State(name=data_dict['name'])
        new_state.save()
        return jsonify(new_state.to_dict()), 201
    # elif request.method == 'PUT':
    if state_object is None:
        abort(404)
    data_dict = request.get_json()
    if data_dict is None:
        abort(400, 'Not a JSON')
    forbidden_list = ['id', 'created_at', 'updated_at']
    for key, value in data_dict.items():
        if key not in forbidden_list:
            setattr(state_object, key, value)
    # change the updated_at attribute
    setattr(state_object, 'updated_at', datetime.utcnow())
    storage.save()
    return jsonify(state_object.to_dict()), 200
