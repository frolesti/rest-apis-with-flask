from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import StoreModel
from schemas import StoreSchema

blp = Blueprint("Stores", __name__, description="Operations on stores")

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
            abort(400, message="Store already exists")
        except SQLAlchemyError:
            abort(500, message="An error occurred while adding the store")
        
            # store_data = request.get_json()
        # if "name" not in store_data:
        #     abort(400, message="Ensure you provide a name for the store")
            
        # for store in stores.values():
        #     if store_data["name"] == store["name"]:
        #         abort(400, message=f"Store already exists")
                
        # store_id = uuid.uuid4().hex
        # store = {**store_data, "id": store_id}
        # stores[store_id] = store
        # return store, 201
        
    
@blp.route("/store/<int:store_id>")
class Store(MethodView):
    
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store
    
            # try:
        #     return stores[store_id]
        # except KeyError:
        #     abort(404, message="Store not found")
    
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted"}, 204
    
            # try:
        #     del stores[store_id]
        #     return {"message": "Store deleted"}, 204
        # except KeyError:
        #     abort(404, message="Store not found")
            
    def put(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        raise NotImplementedError("Update store not implemented")
    
    # store_data = request.get_json()
        # if "name" not in store_data:
        #     abort(400, message="Ensure you provide a name for the store")
            
        # for store in stores.values():
        #     if store_data["name"] == store["name"]:
        #         abort(400, message="Store already exists")
                
        # store = {**store_data, "id": store_id}
        # stores[store_id] = store
        # return store, 201