# api/routes.py

from flask import Blueprint, jsonify, request
from models import User, Post
from price_oracle import PriceOracle

api_routes = Blueprint('api', __name__)
price_oracle = PriceOracle()

@api_routes.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user = User(data['user_id'], data['attributes'])
    return jsonify({"message": "User  created", "user": user.to_dict()}), 201

@api_routes.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.get_user(user_id)
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({"message": "User  not found"}), 404

@api_routes.route('/posts', methods=['POST'])
def create_post():
    data = request.json
    post = Post(data['post_id'], data['user_id'], data['title'], data['content'])
    return jsonify({"message": "Post created", "post": post.to_dict()}), 201

@api_routes.route('/price/<coin_id>', methods=['GET'])
def get_price(coin_id):
    price = price_oracle.get_price(coin_id)
    if price is not None:
        return jsonify({"coin_id": coin_id, "price": price}), 200
    return jsonify({"message": "Price not available"}), 404
