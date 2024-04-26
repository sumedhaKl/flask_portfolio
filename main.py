from flask import render_template, request
from flask_cli import AppGroup #type: ignore
from flask_cors import CORS #type: ignore
from __init__ import app
from model.shopping_model import ShoppingModel  
from projects.projects import app_projects
from api.shopping import shopping_api

# Register CORS for cross-origin requests
CORS(app, supports_credentials=True, origins=['http://localhost:4100', 'http://127.0.0.1:4100', 'https://nighthawkcoders.github.io'])

# Register API blueprint
app.register_blueprint(shopping_api)

# Register app pages
app.register_blueprint(app_projects)

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

# Before request hook to handle CORS
@app.before_request
def before_request():
    allowed_origin = request.headers.get('Origin')
    if allowed_origin in ['http://localhost:4100', 'http://127.0.0.1:4100', 'https://nighthawkcoders.github.io']:
        CORS._origins = allowed_origin

# Custom CLI commands
custom_cli = AppGroup('custom', help='Custom commands')

@custom_cli.command('generate_data')
def generate_data():
    ShoppingModel.init_shopping_model()
    print("Data generated successfully.")

app.cli.add_command(custom_cli)

# Run the application
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8086")