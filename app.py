# app.py

import os

import boto3

from flask import Flask, jsonify, request
app = Flask(__name__)

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
        return jsonify({'error': 'User does not exist'}), 404

    return jsonify({
        'routeId': item.get('routeId').get('S'),
        'name': item.get('name').get('S'),
        'coordinates': item.get('coordinates').get('L')
    })


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
            'coordinates': {'L': [{'NS': c for c in coordinates}]
        }
    )

#     table.put_item(
#         Item={
#             'route_id' = route_id,
#             'name' = name,
#             'coordinates' = coordinates
#         }
#     )

    return jsonify({
        'routeId': route_id,
        'name': name,
        'coordinates': coordinates
    })
