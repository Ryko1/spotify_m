from flask import Blueprint, jsonify, abort, request
from ..models import User, Playlist, Song, Artist, db
from src.python_requests import get_token

bp = Blueprint('artists', __name__, url_prefix='/artists')

@bp.route('', methods=['GET'])
def index():
    try:
        artists = Artist.query.all()
        result = []
        for a in artists:
            result = [a.serialize()]
        return jsonify(result)
    except Exception as e:
        # Log the error and return an error response
        print(str(e))
        return jsonify({'error': str(e)}), 500    
    
@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    a = Artist.query.get_or_404(id, "Artist not found")
    return jsonify(a.serialize())

@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id: int):
    a = Artist.query.get_or_404(id, "Artist not found")

    if 'name' not in request.json and 'genre' not in request.json:
        return abort(400)

    if 'name' in request.json:           
        a.name = request.json['name']
    
    if 'genre' in request.json:
        a.genre = request.json['genre']

    try:
        db.session.add(a)  
        db.session.commit()  
        return jsonify(True)
    except Exception as e:    # --'Exception' must be a specific error(code)
        # something went wrong :(
        print(str(e))
        return jsonify({'error': str(e)}), 500
    
@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    a = Artist.query.get_or_404(id, "Artist not found")
    try:
        db.session.delete(a)  # prepare DELETE statement
        db.session.commit()  # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)