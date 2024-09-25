#!/usr/bin/python3
"""Handles all default RESTful API actions for City objects.
"""

from api.v1.views import app_views
from datetime import datetime
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET', 'POST'])
def cities_by_state(state_id):
    """Retrieves all cities in a certain State

    Args:
        state_id (str): the id of the State object whose cities are to be
        retrieved.

    Returns:
        list: a list of dictionary represantations of each city in a State
    """
    state_object = storage.get(State, state_id)
    if request.method == 'GET':
        if state_object is None:
            abort(404)
        state_cities = [obj.to_dict() for obj in state_object.cities]
        return jsonify(state_cities)
    elif request.method == 'POST':
        if state_object is None:
            abort(404)
        # Create a new city
        # First check if the data is valid JSON
        if request.headers.get('Content-Type') != 'application/json':
            abort(400, "Not a JSON")
        data_dict = request.get_json()
        if data_dict is None:  # Not a valid JSON
            abort(400, "Not a JSON")
        if 'name' not in data_dict:
            abort(400, "Missing name")
        new_city = City(state_id=state_id, name=data_dict['name'])
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET',
                 'DELETE', 'PUT'])
def city_by_id(city_id):
    """Retrieves a city using its id

    Args:
        city_id (str): unique identifier of City to be retrieved.

    Returns:
        dict: Dictionary representation of found City object.
    """
    city_object = storage.get(City, city_id)
    if request.method == 'GET':
        if city_object is None:
            abort(404)
        return jsonify(city_object.to_dict())
    elif request.method == 'DELETE':
        if city_object is None:
            abort(404)
        storage.delete(city_object)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        if city_object is None:
            abort(404)
        # Check if data is valid json
        if request.headers.get('Content-Type') != 'application/json':
            abort(400, 'Not a JSON')
        data_dict = request.get_json()
        if data_dict is None:
            abort(400, 'Not a JSON')
        prohibited_list = ['id', 'created_at', 'updated_at', 'state_id']
        for key, value in data_dict.items():
            if key not in prohibited_list:
                setattr(city_object, key, value)
        setattr(city_object, 'updated_at', datetime.utcnow())
        storage.save()
        return jsonify(city_object.to_dict()), 200
