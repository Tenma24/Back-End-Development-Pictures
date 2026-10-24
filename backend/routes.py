from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = next((p for p in data if p['id'] == id), None)
    return (jsonify(picture), 200) if picture else ({'message': 'picture not found'}, 404)


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.get_json(silent=True)
    if not isinstance(picture, dict) or type(picture.get('id')) is not int:
        return {'message': 'A JSON object with an integer id is required'}, 400
    if any(p['id'] == picture['id'] for p in data):
        return {'Message': f"picture with id {picture['id']} already present"}, 302
    fields = ('pic_url', 'event_country', 'event_state', 'event_city', 'event_date')
    if not all(isinstance(picture.get(k), str) and picture[k] for k in fields):
        return {'message': 'Missing picture fields'}, 400
    data.append({k: picture[k] for k in ('id', *fields)})
    return jsonify(data[-1]), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture = next((p for p in data if p['id'] == id), None)
    if picture is None:
        return {'message': 'picture not found'}, 404
    changes = request.get_json(silent=True)
    if not isinstance(changes, dict) or changes.get('id', id) != id:
        return {'message': 'Invalid picture'}, 400
    for key in ('pic_url', 'event_country', 'event_state', 'event_city', 'event_date'):
        if key in changes and not isinstance(changes[key], str):
            return {'message': 'Invalid picture field'}, 400
    picture.update({k: v for k, v in changes.items() if k in picture and k != 'id'})
    return jsonify(picture), 200

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    picture = next((p for p in data if p['id'] == id), None)
    if picture is None:
        return {'message': 'picture not found'}, 404
    data.remove(picture)
    return '', 204
