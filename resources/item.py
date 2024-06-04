from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", __name__, description="Operations on items")

@blp.route("/item")
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()
    
    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        try: 
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while adding the item")
        return item, 201
            
                    # item_data = request.get_json()
        # if ("price" not in item_data or "name" not in item_data or "name" not in item_data):
        #     abort(400, message="Ensure you provide a name and price for the item")
            
        # for item in items.values():
        #     if item_data["name"] == item["name"] and item_data["store_id"] == item["store_id"]:
        #         abort(400, message="Item already exists")
                
        # item_id = uuid.uuid4().hex
        # item = {**item_data, "id": item_id}
        # items[item_id] = item
        # return item, 201
            
            
    
    
@blp.route("/item/<int:item_id>")
class item(MethodView):
    
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item
            # try:
        #     return items[item_id]
        # except KeyError:
        #     abort(404, message="Item not found")
    
    @jwt_required()
    def delete(self, item_id):
        jwt = get_jwt()
        
        if not jwt.get("is_admin"):
            abort(401, message="You are not authorized to delete this item")
            
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted"}, 204
    
            # try:
        #     del items[item_id]
        #     return {"message": "Item deleted"}, 204
        # except KeyError:
        #     abort(404, message="Item not found")
            
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)    
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)
        db.session.add(item)
        db.session.commit()
        return item
    
    # item_data = request.get_json()
        # if "price" not in item_data or "name" not in item_data:
        #    abort(400, message="Ensure you provide a name and price for the item")
        # try: 
        #     item = items[item_id]
            
        #     item |= item_data
        #     return item, 201
        # except KeyError:
        #     abort(404, message="Item not found")
            
       