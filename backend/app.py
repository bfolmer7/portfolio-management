from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from database import db
import requests
import os

def create_app():
    app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/portfoliomanager'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    CORS(app)

    with app.app_context():
        from models import StockData
        db.create_all()

    @app.route('/')
    def index():
        return send_from_directory(app.static_folder, 'index.html')

    @app.route('/api/stock', methods=['GET'])
    def get_stock_data():
        symbol = request.args.get('symbol', default='IBM', type=str)
        interval = request.args.get('interval', default='5min', type=str)
        api_key = os.environ.get('ALPHA_VANTAGE_API_KEY', 'default_api_key')

        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&apikey={api_key}'
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()

            stock_entry = StockData(symbol=symbol, data=data)
            db.session.add(stock_entry)
            db.session.commit()

            return jsonify(data)
        else:
            return jsonify({"error": "Error fetching data from API"}), response.status_code

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
