from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from config import DevApplication
from db import db
from resources.routes import routes

app = Flask(__name__)
app.config.from_object(DevApplication)
db.init_app(app)

migrate = Migrate(app, db)
api = Api(app)

[api.add_resource(*r) for r in routes]

if __name__ == "__main__":
    app.run()
