#!/usr/bin/python3
"""Index file"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """Returns the API status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats_by_type():
    """Retrieves the number of each objects by type"""
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User
    from models import storage

    stats_dict = {
                    "amenities": Amenity,
                    "cities": City,
                    "places": Place,
                    "reviews": Review,
                    "states": State,
                    "users": User
                    }
    for key, value in stats_dict.items():
        stats_dict[key] = storage.count(value)
    return jsonify(stats_dict)
