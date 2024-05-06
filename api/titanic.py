from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from model.titanic_model import TitanicModel

titanic_api = Blueprint('titanic_api', __name__, url_prefix='/api/titanic')
api = Api(titanic_api)

class TitanicAPI:
    class _Predict(Resource):
        
        def post(self):
            
            passenger = request.get_json()

            # Get the singleton instance of the TitanicModel
            titanicModel = TitanicModel.get_instance()
            # Predict the survival probability of the passenger
            response = titanicModel.predict(passenger)

            # Return the response as JSON
            return jsonify(response)

    api.add_resource(_Predict, '/predict')