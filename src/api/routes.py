from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, Users, Comments
from api.utils import generate_sitemap, APIException
from flask_cors import CORS


api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/user/<int:user_id>/comments', methods=['GET', 'POST'])
def handle_user_comments(user_id):
    response_body = {}
    user = Users.query.get(user_id)
    if not user:
            response_body['error'] = 'User not found'
            return response_body, 404 # Si no hay usuario ya devuelve un 404
    if request.method == 'GET':
        comments = [{'id': comment.id, 'text': comment.text} for comment in user.comments] # Mete todos los comentarios del usuario en 'comments'
        response_body['message'] = 'User found'
        response_body['results'] = comments # Mete todos los comentarios en 'results'
        response_body['username'] = user.username # Devuelve tambien el nombre de usuario
        return response_body, 200
        
    elif request.method == 'POST':
        data = request.json
        comment = Comments(text=data['text'], user_id=user_id)
        db.session.add(comment)
        db.session.commit()
        response_body['message'] = 'Comment was successfully saved'
        response_body['comment'] = data['text']
        return response_body, 201
