from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os
import requests

# Initialize SQLAlchemy without passing the Flask app object
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class StockData(db.Model):
    __tablename__ = 'stock_data'
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    data = db.Column(db.JSON, nullable=False)

def create_app():
    # Initialize the Flask application
    app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_COOKIE_NAME'] = 'investmentportfoliomanager'  # Replace 'myapp_session' with a name of your choice
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SECURE'] = True  # Use with HTTPS only

    # Bind SQLAlchemy to the Flask app
    db.init_app(app)
    CORS(app)

    with app.app_context():
        db.create_all()

    # Stock API Logic
    @app.route('/api/stock', methods=['GET'])
    def get_stock_data():
        symbol = request.args.get('symbol', default='IBM', type=str)
        interval = request.args.get('interval', default='5min', type=str)
        api_key = 'BNGIKZISI5NR3ACW'  # Replace with your actual API key

        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&apikey={api_key}'
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            return jsonify(data)
        else:
            return jsonify({"error": "Error fetching data from Alpha Vantage"}), response.status_code

    # Signup Logic
    @app.route('/signup', methods=['POST'])
    def signup():
        data = request.get_json()
        username = data['username']
        password = data['password']

        if User.query.filter_by(username=username).first():
            return jsonify({"message": "Username already exists"}), 409

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User created successfully"}), 201

    # Login Logic
    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"message": "Invalid username or password"}), 401

    # Serve static files (React front-end)
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        return send_from_directory(app.static_folder, 'index.html')



    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

