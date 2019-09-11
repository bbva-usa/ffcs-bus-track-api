# app.py

import os

import boto3

from boto3.dynamodb import types
from flask import Flask, jsonify, request

app = Flask(__name__)
serializer = types.TypeSerializer()
deserializer = types.TypeDeserializer()

ROUTES_TABLE = os.environ['ROUTES_TABLE']
client = boto3.client('dynamodb')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(ROUTES_TABLE)

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/routes/<string:route_id>")
def get_route(route_id):
    resp = client.get_item(
        TableName=ROUTES_TABLE,
        Key={
            'routeId': { 'S': route_id }
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
    _resp = deserializer.deserialize({'L': [{'M': i for i in items}]})
    return jsonify(_resp)



@app.route("/routes", methods=["POST"])
def create_route():
    route_id = request.json.get('routeId')
    name = request.json.get('name')
    coordinates = request.json.get('coordinates')
    print(request)
    if not route_id or not name:
        return jsonify({'error': 'Please provide routeId and name'}), 400

    resp = client.put_item(
        TableName=ROUTES_TABLE,
        Item={
            'routeId': {'S': route_id },
            'name': {'S': name },
            'coordinates': serializer.serialize(coordinates)
#             'coordinates': {'L': [{'M': c for c in coordinates}]}
        }
    )

    return jsonify({
        'routeId': route_id,
        'name': name,
        'coordinates': coordinates
    })
