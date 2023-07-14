import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores, items

blp = Blueprint("Items", __name__, description="Operation on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):

    def get(self, item_id):
        try:
            return items[item_id], 201
        except KeyError:
            return abort(404, message="Item not found")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted"}
        except KeyError:
            return abort(404, message="Item not found")

    def put(self, item_id):
        item_data = request.get_json()
        if 'price' not in item_data or 'name' not in item_data:
            abort(400, message="Bad request")
        try:
            item = items[item_id]
            for key in item.keys():
                if key in item_data.keys():
                    item[key] = item_data[key]
            return item
        except KeyError:
            return abort(404, message="Item not found")


@blp.route("/item")
class ItemList(MethodView):

    def get(self):
        return {"items": list(items.values())}

    def post(self):
        item_data = request.get_json()
        if (
                "price" not in item_data
                or "store_id" not in item_data
                or "name" not in item_data
        ):
            abort(400, message="Bad request, make sure 'price, 'store_id', 'name' "
                               "included in the json payload")

        for item in items.values():
            if (item_data["name"] == item["name"]
                    and item_data["store_id"] == item["store_id"]):
                abort(400, "Item already existed")

        if item_data["store_id"] not in stores:
            return abort(404, message="Store not found")

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item
        return item, 201