#!/usr/bin/python3
"""Handles all default RESTFul API actions for Review objects"""

from api.v1.views import app_views
from datetime import datetime
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['GET', 'POST'])
def reviews_by_place(place_id):
    """Handles some RESTFul API actions for Review objects depending on their
    place_id"""
    place_object = storage.get(Place, place_id)
    if place_object is None:
        abort(404)
    if request.method == 'GET':
        place_reviews_list = place_object.reviews
        place_reviews_dicts = [
                                review_obj.to_dict()
                                for review_obj in place_reviews_list
                               ]
        return jsonify(place_reviews_dicts)
    elif request.method == 'POST':
        if request.headers.get('Content-Type') != 'application/json':
            abort(400, 'Not a JSON')
        data_dict = request.get_json()
        if data_dict is None:
            abort(400, 'Not a JSON')
        if 'user_id' not in data_dict:
            abort(400, 'Missing user_id')
        if storage.get(User, data_dict['user_id']) is None:
            abort(404)
        if 'text' not in data_dict:
            abort(400, 'Missing text')
        new_review = Review(place_id=place_id, user_id=data_dict['user_id'],
                            text=data_dict['text'])
        new_review.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET',
                 'DELETE', 'PUT'])
def review_by_id(review_id):
    """Handles some RESTFul API actions for Review objects depending on
    their id.
    """
    review_object = storage.get(Review, review_id)
    if review_object is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(review_object.to_dict())
    elif request.method == 'DELETE':
        review_object.delete()
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        if request.headers.get('Content-Type') != 'application/json':
            abort(400, 'Not a JSON')
        data_dict = request.get_json()
        if data_dict is None:
            abort(400, 'Not a JSON')
        forbidden_list = ['id', 'user_id', 'place_id',
                          'created_at', 'updated_at']
        for key, value in data_dict.items():
            if key == 'text':
                setattr(review_object, key, value)
        setattr(review_object, 'updated_at', datetime.utcnow())
        storage.save()
        return jsonify(review_object.to_dict()), 200
