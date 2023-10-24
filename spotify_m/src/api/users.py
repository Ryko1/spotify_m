from flask import Blueprint, jsonify, abort, request
from ..models import User, Playlist, Song, Artist, db
import hashlib
import secrets

bp = Blueprint('users', __name__, url_prefix='/users')

def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()

@bp.route('', methods=['GET'])
def index():
    try:
        users = User.query.all()
        result = []
        for u in users:
            result = [u.serialize()]
        return jsonify(result)
    except Exception as e:
        # Log the error and return an error response
        print(str(e))
        return jsonify({'error': str(e)}), 500    

@bp.route('', methods=['POST'])
def create():
    # req body must contain user_id and content
    if 'username' not in request.json or 'password' not in request.json:
        return abort(400, 'Username/Password not found')
    
    u = User(
        username=request.json['username'],
        password=scramble(request.json['password'])
    )

    db.session.add(u)  # prepare CREATE statement
    db.session.commit()  # execute CREATE statement

    return jsonify(u.serialize())

@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id: int):
    u = User.query.get_or_404(id, "User not found")

    if 'username' not in request.json or 'password' not in request.json:
        return abort(400)
    
    if 'username' in request.json:
        if len(request.json['username']) > 5:
            return abort(400, 'Username length is invalid')
        else:
            u.username = request.json['username']

    if 'password' in request.json:
        if len(request.json['password']) > 8:
            return abort(400, 'Password length is invalid')
        else:
            u.password = request.json['password']   

@bp.route('/user_playlist/<int:id>', methods=['GET'])
def user_playlist(id: int):
    u = User.query.get_or_404(id)
    user_playlists = u.playlists
    result = [playlist.serialize() for playlist in user_playlists]
    return jsonify(result)

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    u = User.query.get_or_404(id, "User not found")
    try:
        db.session.delete(u)  # prepare DELETE statement
        db.session.commit()  # execute DELETE statement
        return jsonify(True)
    except Exception as e:
        # Log the error and return an error response
        print(str(e))
        return jsonify({'error': str(e)}), 500 