import sys

sys.path.append('/home/sumi/vscode/flask_portfolio')

from flask import Blueprint, request
from flask_restful import Api, Resource #type: ignore
from model.shopping_model import ShoppingModel 

shopping_api = Blueprint('shopping_api', __name__, url_prefix='/api/shopping')
api = Api(shopping_api)

class Predict(Resource):
    def post(self):
        data = request.json
        shopping_model = ShoppingModel.get_instance()
        result = shopping_model.predict(data)
        return {'message': 'Predict resource', 'total_price': result}

api.add_resource(Predict, '/predict')