import sys

sys.path.append('/home/sumi/vscode/flask_portfolio')

from flask import request
from flask_restful import Resource
from flask_cors import cross_origin
from model.shopping_model import ShoppingModel 

class Predict(Resource):
    @cross_origin(origins=['http://localhost:4100', 'http://127.0.0.1:4100', 'https://nighthawkcoders.github.io'])
    def post(self):
        data = request.json
        print("Received data:", data)
        
        shopping_model = ShoppingModel.get_instance()
        
        result = shopping_model.predict(data)
        
        return {'total_price': result['total_price']}