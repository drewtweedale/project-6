"""
Resource: BrevetsResource
"""
from flask import Response, request
from flask_restful import Resource

from database.models import Brevet

class BrevetsResource(Resource):
    def get(self):
        json_object = Brevet.objects().to_json()
        return Response(json_object, mimetype="application/json", status=200)

    def post(self):
        # Read the entire request body as a JSON
        # This will fail if the request body is NOT a JSON.
        input_json = request.json
        result = Brevet(**input_json).save()
        return {'_id': str(result.id)}, 200
    
