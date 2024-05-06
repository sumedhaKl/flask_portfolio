from flask import Flask, render_template
from flask_cors import CORS
from flask_restful import Api
from api.shopping import Predict

app = Flask(__name__)

# Register CORS for cross-origin requests
CORS(app, supports_credentials=True, origins=['http://localhost:4100', 'http://127.0.0.1:4100', 'https://nighthawkcoders.github.io'])

api = Api(app)

# Register API resource
api.add_resource(Predict, '/api/shopping/predict')

# Error handler for 404 Not Found
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Home route
@app.route('/')
def index():
    return render_template("index.html")

# Table route
@app.route('/table/')
def table():
    return render_template("table.html")

# Run the application
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8086")