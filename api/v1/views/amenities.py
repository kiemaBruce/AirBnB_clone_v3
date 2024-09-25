#!/usr/bin/python3
"""Handles all default RESTFul API actions for Amenity objects"""

from api.v1.views import app_views
from datetime import datetime
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False, methods=['GET', 'POST'])
@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def amenities(amenity_id=None):
    """Handles some RESTFul API actions for Amenity objects"""
    if amenity_id:
        amenity_object = storage.get(Amenity, amenity_id)
    if request.method == 'GET':  # Retrieve all amenities
        if amenity_id is None:
            amenities_objs = storage.all(Amenity).values()
            amenities_list = [obj.to_dict() for obj in amenities_objs]
            return jsonify(amenities_list)
        elif amenity_object is None:  # No such amenity exists
            abort(404)
        # Retrieve the specific amenity because it exists
        return jsonify(amenity_object.to_dict())
    elif request.method == 'DELETE':
        if amenity_object is None:
            abort(404)
        amenity_object.delete()
        storage.save()
        return jsonify({}), 200
    elif request.method == 'POST':
        # Create new amenity object
        if request.headers.get('Content-Type') != 'application/json':
            abort(400, 'Not a JSON')
        data_dict = request.get_json()
        if data_dict is None:
            abort(400, 'Not a JSON')
        if 'name' not in data_dict:
            abort(400, 'Missing name')
        new_amenity = Amenity(name=data_dict['name'])
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201
    elif request.method == 'PUT':
        if amenity_object is None:
            abort(404)
        if request.headers.get('Content-Type') != 'application/json':
            abort(400, 'Not a JSON')
        data_dict = request.get_json()
        if data_dict is None:
            abort(400, 'Not a JSON')
        forbidden_list = ['id', 'created_at', 'updated_at']
        for key, value in data_dict.items():
            if key not in forbidden_list:
                setattr(amenity_object, key, value)
        # change the updated_at attribute
        setattr(amenity_object, 'updated_at', datetime.utcnow())
        storage.save()
        return jsonify(amenity_object.to_dict()), 200
