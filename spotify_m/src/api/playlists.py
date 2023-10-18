from flask import Blueprint, jsonify, abort, request
from ..models import User, Playlist, Song, Artist, db

bp = Blueprint('playlists', __name__, url_prefix='/playlists')

@bp.route('', methods=['GET'])
def index():
    try:
        playlist = Playlist.query.all()
        result = []
        for p in playlist:
            result = [p.serialize()]
        return jsonify(result)
    except Exception as e:
        # Log the error and return an error response
        print(str(e))
        return jsonify({'error': str(e)}), 500 

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    p = Playlist.query.get_or_404(id, "Playlist not found")
    return jsonify(p.serialize())

@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id: int):
    p = Playlist.query.get_or_404(id, "Playlist not found")

    if 'name' not in request.json:
        return abort(400)

    if 'name' in request.json:           
        p.name = request.json['name']

    try:
        db.session.add(p)  # prepare DELETE statement
        db.session.commit()  # execute DELETE statement
        return jsonify(True)
    except Exception as e:    # --'Exception' must be a specific error(code)
        # something went wrong :(
        print(str(e))
        return jsonify({'error': str(e)}), 500 
    
@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    p = Playlist.query.get_or_404(id, "Playlist not found")
    try:
        db.session.delete(p)  # prepare DELETE statement
        db.session.commit()  # execute DELETE statement
        return jsonify(True)
    except Exception as e:
        # Log the error and return an error response
        print(str(e))
        return jsonify({'error': str(e)}), 500 