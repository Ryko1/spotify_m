from flask import Blueprint, jsonify, abort, request
from ..models import User, Playlist, Song, Artist, db

bp = Blueprint('songs', __name__, url_prefix='/songs')

@bp.route('', methods=['GET'])
def index():
    try:
        songs = Song.query.all()
        result = []
        for s in songs:
            result = [s.serialize()]
        return jsonify(result)
    except Exception as e:
        # Log the error and return an error response
        print(str(e))
        return jsonify({'error': str(e)}), 500 

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    s = Song.query.get_or_404(id, "Song not found")
    return jsonify(s.serialize())

@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id: int):
    s = Song.query.get_or_404(id, "Song not found")

    if 'title' not in request.json:
        return abort(400) 
    
    if 'title' in request.json:           
        s.name = request.json['name']

    try:
        db.session.add(s)  # prepare DELETE statement
        db.session.commit()  # execute DELETE statement
        return jsonify(True)
    except Exception as e:    # --'Exception' must be a specific error(code)
        # something went wrong :(
        print(str(e))
        return jsonify({'error': str(e)}), 500 
    

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    s = Song.query.get_or_404(id, "Song not found")
    try:
        db.session.delete(s)  # prepare DELETE statement
        db.session.commit()  # execute DELETE statement
        return jsonify(True)
    except Exception as e:
        # Log the error and return an error response
        print(str(e))
        return jsonify({'error': str(e)}), 500 