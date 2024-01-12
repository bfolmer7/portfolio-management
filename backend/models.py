from database import db

class StockData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(50), nullable=False)
    data = db.Column(db.JSON, nullable=False)

    def __repr__(self):
        return f'<StockData {self.symbol}>'
