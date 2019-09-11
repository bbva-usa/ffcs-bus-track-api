# app.py

import os

import boto3

from boto3.dynamodb import types
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
serializer = types.TypeSerializer()
deserializer = types.TypeDeserializer()

ROUTES_TABLE = os.environ['ROUTES_TABLE']
POINTS_OF_INTEREST_TABLE = os.environ['POINTS_OF_INTEREST_TABLE']
client = boto3.client('dynamodb')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(ROUTES_TABLE)
pointsOfInterestTable = dynamodb.Table(POINTS_OF_INTEREST_TABLE)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/routes/<string:route_id>")
def get_route(route_id):
    resp = client.get_item(
        TableName=ROUTES_TABLE,
        Key={
            'routeId': {'S': route_id}
        }
    )

    item = resp.get('Item')
    if not item:
        return jsonify({'error': 'Route does not exist'}), 404

    _resp = deserializer.deserialize({'M': item})
    return jsonify(_resp)


@app.route("/routes")
def get_routes():
    resp = client.scan(
        TableName=ROUTES_TABLE,
    )
    items = resp.get('Items')
    if not items:
        return jsonify({'error': 'Route does not exist'}), 404
    _resp = [ deserializer.deserialize({'M': i}) for i in items ]
    return jsonify(_resp)


@app.route("/routes", methods=["POST"])
def create_route():
    route_id = request.json.get('routeId')
    name = request.json.get('name')
    timeOfDay = request.json.get('timeOfDay')
    coordinates = request.json.get('coordinates')
    print(request)
    if not route_id or not name:
        return jsonify({'error': 'Please provide routeId and name'}), 400

    resp = client.put_item(
        TableName=ROUTES_TABLE,
        Item={
            'routeId': {'S': route_id},
            'name': {'S': name},
            'timeOfDay': {'S': timeOfDay},
            'coordinates': serializer.serialize(coordinates)
        }
    )

    return jsonify({
        'routeId': route_id,
        'name': name,
        'coordinates': coordinates
    })


@app.route("/routes", methods=["DELETE"])
def delete_routes():
    scan = table.scan()
    with table.batch_writer() as batch:
        for each in scan['Items']:
            batch.delete_item(
                Key={
                    'routeId': each['routeId']
                }
            )
    return jsonify({})





@app.route("/pointsOfInterest/<string:pointOfInterestId>")
def get_point_of_interest(pointOfInterestId):
    resp = client.get_item(
        TableName=POINTS_OF_INTEREST_TABLE,
        Key={
            'pointOfInterestId': {'S': pointOfInterestId}
        }
    )

    item = resp.get('Item')
    if not item:
        return jsonify({'error': 'Point of interest does not exist'}), 404

    _resp = deserializer.deserialize({'M': item})
    return jsonify(_resp)


@app.route("/pointsOfInterest")
def get_points_of_interest():
    resp = client.scan(
        TableName=POINTS_OF_INTEREST_TABLE,
    )
    items = resp.get('Items')
    if not items:
        return jsonify({'error': 'Point of interest does not exist'}), 404
    _resp = [ deserializer.deserialize({'M': i}) for i in items ]
    return jsonify(_resp)

@app.route("/pointsOfInterest", methods=["POST"])
def create_point_of_interest():
    pointOfInterestId = request.json.get('pointOfInterestId')
    name = request.json.get('name')
    location = request.json.get('location')
    latitude = request.json.get('latitude')
    longitude = request.json.get('longitude')
    poitype = request.json.get('type')
    if not pointOfInterestId or not name:
        return jsonify({'error': 'Please provide pointOfInterestId and name'}), 400

    resp = client.put_item(
        TableName=POINTS_OF_INTEREST_TABLE,
        Item={
            'pointOfInterestId': {'S': pointOfInterestId},
            'name': {'S': name},
            'location': {'S': location},
            'latitude': {'S': latitude},
            'longitude': {'S': longitude},
            'type': {'S': poitype}
        }
    )

    return jsonify({
        'pointOfInterestId': pointOfInterestId,
        'name': name,
        'location': location,
        'latitude': latitude,
        'longitude': longitude,
        'type': poitype
    })

@app.route("/pointsOfInterest", methods=["DELETE"])
def delete_points_of_interest():
    scan = pointsOfInterestTable.scan()
    with pointsOfInterestTable.batch_writer() as batch:
        for each in scan['Items']:
            batch.delete_item(
                Key={
                    'pointOfInterestId': each['pointOfInterestId']
                }
            )
    return jsonify({})
