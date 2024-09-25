#!/usr/bin/python3
"""Handles all default RESTFul API actions for Place objects"""

from api.v1.views import app_views
from datetime import datetime
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET', 'POST'])
def places_by_city(city_id):
    """Returns all places in a given City

    city_id (str): the unique identifier of the City whose places are to be
                   returned

    Returns:
        list: A list of dictionary representations of all places in a city
    """
    city_object = storage.get(City, city_id)
    if city_object is None:  # No such city exists
        abort(404)
    if request.method == 'GET':
        # Retrieve places in that city
        places_list = [
                        place.to_dict()
                        for place in city_object.places
                        ]
        return jsonify(places_list)
    elif request.method == 'POST':
        # create new Place object
        if request.headers.get('Content-Type') != 'application/json':
            abort(400, 'Not a JSON')
        data_dict = request.get_json()
        if data_dict is None:
            abort(400, 'Not a JSON')
        if 'user_id' not in data_dict:
            abort(400, 'Missing user_id')
        if storage.get(User, data_dict['user_id']) is None:  # No such user
            abort(404)
        if 'name' not in data_dict:
            abort(400, 'Missing name')
        new_place = Place(city_id=city_id, user_id=data_dict['user_id'],
                          name=data_dict['name'])
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET',
                 'DELETE', 'PUT'])
def place_by_id(place_id):
    """Performs a number of RESTFul API actions for Place objects.

    These include retrieval of a place by id, deletion of a place with a
    specific id, and updating a place that has a specific id.

    Args:
        place_id (str): the unique identifier of the place object.
    """
    place_object = storage.get(Place, place_id)
    if place_object is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(place_object.to_dict())
    elif request.method == 'DELETE':
        place_object.delete()
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        # Update existing Place object
        if request.headers.get('Content-Type') != 'application/json':
            abort(400, 'Not a JSON')
        data_dict = request.get_json()
        if data_dict is None:
            abort(400, 'Not a JSON')
        forbidden_list = ['id', 'user_id', 'city_id', 'created_at',
                          'updated_at']
        allowed_attrs = ['name', 'description', 'number_rooms',
                         'number_bathrooms', 'max_guest', 'price_by_night',
                         'latitude', 'longitude']
        for key, value in data_dict.items():
            if key not in forbidden_list and key in allowed_attrs:
                setattr(place_object, key, value)
        setattr(place_object, 'updated_at', datetime.utcnow())
        storage.save()
        return jsonify(place_object.to_dict()), 200
