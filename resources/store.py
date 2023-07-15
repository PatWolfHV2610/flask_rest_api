import uuid

from db import db
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import StoreModel
from schemas import StoreSchema, StoreUpdateSchema
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

blp = Blueprint("Store", __name__, description="Operation on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):

    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted"}

    @blp.arguments(StoreUpdateSchema)
    @blp.response(200, StoreSchema)
    def put(self, store_data, store_id):
        store = StoreModel.query.get(store_id)
        if store:
            store.name = store_data["name"]
        else:
            store = StoreModel(id=store_id, **store_data)
        db.session.add(store)
        db.session.commit()
        return store

@blp.route("/store")
class StoreList(MethodView):

    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with same name already insert")
        except SQLAlchemyError:
            abort(500, message="An error occur while creating the store")
        return store
