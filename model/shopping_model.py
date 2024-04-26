from flask_sqlalchemy import SQLAlchemy
from flask import current_app
from sklearn.tree import DecisionTreeClassifier #type: ignore
from sklearn.linear_model import LogisticRegression #type: ignore
from sklearn.preprocessing import OneHotEncoder #type: ignore
import pandas as pd
from sqlite3 import IntegrityError

db = SQLAlchemy()

class ShoppingModel(db.Model): #type: ignore
    _instance = None
    __tablename__ = 'shoppingorders'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String, nullable=False)
    items_ordered = db.Column(db.String)
    quantity_ordered = db.Column(db.String)
    price = db.Column(db.String)
    total = db.Column(db.String)

    def __init__(self, category=None, items_ordered=None, quantity_ordered=None, price=None, total=None):
        self.category = category
        self.items_ordered = items_ordered
        self.quantity_ordered = quantity_ordered
        self.price = price
        self.total = total

        self.model = None
        self.dt = None
        self.features = ["order_id", "category", "items_ordered", "quantity_ordered", "price", "total"]
        self.shopping_data = None
        self.encoder = OneHotEncoder(handle_unknown='ignore')

        self._clean()
        self._train()

    def _clean(self):
        with current_app.app_context():
            query = "SELECT * FROM shoppingorders"
            self.shopping_data = pd.read_sql_query(query, db.session.bind)
        if self.shopping_data.empty:
            raise ValueError("No data available for training.")

    def _train(self):
        X = self.shopping_data[self.features]
        y = self.shopping_data['price']

        self.model = LogisticRegression(max_iter=1000)
        self.model.fit(X, y)

        self.dt = DecisionTreeClassifier()
        self.dt.fit(X, y)
       
    @classmethod    
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        cls._instance._clean()
        cls._instance._train()
        return cls._instance

    def predict(self, data):
        selected_items = [product['price'] for product in data]
        total_price = sum(selected_items)
        return total_price

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.rollback()
            return None

    @classmethod
    def get_by_id(cls, item_id):
        return cls.query.get(id=item_id)

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def update(self, new_data):
        for key, value in new_data.items():
            setattr(self, key, value)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def initShoppingModel():
        with current_app.app_context():
            db.create_all()
            order = ShoppingModel(category="Food", items_ordered="bread", quantity_ordered=1, price=2, total=3)
            try:
                order.create()
            except IntegrityError:
                db.session.rollback()
                
        if __name__ == "__main__":
            ShoppingModel.init_shopping_model()