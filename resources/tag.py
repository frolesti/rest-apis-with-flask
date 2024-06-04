from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TagModel, StoreModel, ItemModel
from schemas import TagSchema, TagAndItemSchema

blp = Blueprint("Tags", __name__, description="Operations on tags")

@blp.route("/store/<int:store_id>/tag")

class TagsInStore(MethodView):
    
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()
    
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        tag = TagModel(**tag_data, store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit()
            
        except SQLAlchemyError as e:
            abort(500, message=str(e))
            
        return tag, 201
    
        # if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == tag_data["name"]).first():
        #abort(400, message="Tag already exists")
        
        
    @blp.route("/item/<int:item_id>/tag/<int:tag_id>")
    class LinkTagsToItem(MethodView):
        @blp.response(201, TagSchema)
        def post(self, item_id, tag_id):
            item = ItemModel.query.get_or_404(item_id)
            tag = TagModel.query.get_or_404(tag_id)
        
            item.tags.append(tag)
            
            try: 
                db.session.add(item)
                db.session.commit()
            except SQLAlchemyError:
                abort(500, message="An error occurred while adding the tag to the item")
            return tag, 201

        @blp.response(204, TagAndItemSchema)
        def delete(self, item_id, tag_id):
            item = ItemModel.query.get_or_404(item_id)
            tag = TagModel.query.get_or_404(tag_id)
        
            item.tags.remove(tag)
            
            try: 
                db.session.add(item)
                db.session.commit()
            except SQLAlchemyError:
                abort(500, message="An error occurred while substracting the tag to the item")
            return {"message": "Tag removed from item", "item": item, "tag": tag}, 204
    
    @blp.route("/tag/<int:tag_id>")
    class Tag(MethodView):
        @blp.response(200, TagSchema)
        def get(self, tag_id):
            tag = TagModel.query.get_or_404(tag_id)
            return tag


        @blp.response(204, description="Deletes a tag if no item is tagged with it", example={"message": "Tag deleted."})
        @blp.alt_response(404, description="Tag not found", example={"message": "Tag not found."})
        @blp.alt_response(400, description="Tag is linked to an item", example={"message": "Tag is linked to an item."})
        
        def delete(self, tag_id):
            tag = TagModel.query.get_or_404(tag_id)
            if not tag.items:
                db.session.delete(tag)
                db.session.commit()
                return {"message": "Tag deleted"}, 204
            abort(400, message="Could not delete tag. Tag is linked to an item.")