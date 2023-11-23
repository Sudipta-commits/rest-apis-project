#import uuid
#from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import ItemModel
from schemas import ItemSchema,ItemUpdateSchema
from flask_jwt_extended import jwt_required,get_jwt


# http://localhost:5000/swagger-ui

blp=Blueprint("items",__name__,description="Operations on Items")

@blp.route("/item/<string:item_id>")
class item(MethodView):
    @jwt_required()
    @blp.response(200,ItemSchema)
    def get(self,item_id):
     item=ItemModel.query.get_or_404(item_id)
     return item

    @jwt_required()
    def delete(self,item_id):
      jwt = get_jwt()
      if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
      item=ItemModel.query.get_or_404(item_id)
      db.session.delete(item)
      db.session.commit()
      return {"message":"Item deleted"}
       
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200,ItemSchema)
    def put(self,item_data,item_id): 
       
       item=ItemModel.query.get(item_id)
       if item:
          item.name=item_data["name"]
          item.price=item_data["price"]
       else:
          item=ItemModel(id=item_id,**item_data)
       try:
        db.session.add(item)
        db.session.commit()

       except SQLAlchemyError:
        abort(500,message="An error occured while updating the item")   
       return item   

@blp.route("/item")
class itemlist(MethodView):
   @jwt_required() 
   @blp.arguments(ItemSchema)
   @blp.response(201,ItemSchema)
   def post(self,item_data):
     
     item=ItemModel(**item_data)
     try:
        db.session.add(item)
        db.session.commit()

     except SQLAlchemyError:
        abort(500,message="An error occured while inserting the item")   
     return item
   
   @blp.response(200,ItemSchema(many=True))
   @jwt_required()
   def get(self):
      return ItemModel.query.all()
              
                