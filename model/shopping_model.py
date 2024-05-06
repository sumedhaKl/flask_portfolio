from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import pandas as pd
from sklearn.tree import DecisionTreeClassifier 
from sklearn.linear_model import LogisticRegression

db = SQLAlchemy()

class ShoppingModel(db.Model):
    
    _instance = None
    __tablename__ = 'shoppingorders'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String, nullable=False)
    items_ordered = db.Column(db.String)
    quantity_ordered = db.Column(db.String)
    price_per_item = db.Column(db.String) 

    def __init__(self):
        self.model = None
        self.dt = None
        self.features = ["category", "items_ordered", "quantity_ordered", "price_per_item"]
        self.target = "total_price"
        self.shopping_data = 'instance/volumes/shoppingorders.db'
        self.encoder = None  

        self._clean()
        self._train()

    def _clean(self):
        try:
            engine = create_engine(f'sqlite:///{self.shopping_data}')
            df = pd.read_sql_table(self.__tablename__, engine)

            required_columns = self.features + [self.target]
            if all(col in df.columns for col in required_columns):
                df = df[required_columns]
                df.dropna(inplace=True)
                if 'price_per_item' not in df.columns:
                    raise ValueError("Error: 'price_per_item' column not found in the dataframe.")
                self.shopping_data = df
                print("Data cleaning successful.")
                print("DataFrame columns:", df.columns)
            else:
                raise ValueError("Error: Required columns not found in the dataframe.")
        except Exception as e:
            print(f"Error cleaning data: {e}")

    def _train(self):
        try:
            X = self.shopping_data[self.features]
            y = self.shopping_data[self.target]

            self.model = LogisticRegression(max_iter=1000)
            self.model.fit(X, y)

            self.dt = DecisionTreeClassifier()
            self.dt.fit(X, y)
        except Exception as e:
            print(f"Error training model: {e}")

    @classmethod    
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def predict(self, input_data):
        try:
            price_per_item = int(input_data["price_per_item"])
            total_price = price_per_item
            return {'total_price': total_price}
        except KeyError:
            print("Error: 'price_per_item' key not found in input data.")
            return {'total_price': None}
        except ValueError:
            print("Error: 'price_per_item' value is not a valid integer.")
            return {'total_price': None}
    
    def feature_weights(self):
        importances = self.dt.feature_importances_
        return {feature: importance for feature, importance in zip(self.features, importances)}