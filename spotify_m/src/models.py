import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

users_followers_table = db.Table(
    'users_followers', 
    db.Column(
        'user_id', db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True
    ),

    db.Column(
        'followee_id', db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True
    )
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=True)
    playlist_id = db.relationship('playlist', backref='users', lazy=True)
    follower = db.relationship(
        'followers',
        secondary=users_followers_table,
        primaryjoin=(users_followers_table.c.followee_id == id),
        secondaryjoin=(users_followers_table.c.user_id == id),
        backref=db.backref('followee', lazy='dynamic'),
        lazy='dynamic'
    )
    
users_playlists_table = db.Table(
    'users_playlists',
    db.Column(
        'user_id', db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True
    ),

    db.Column(
        'playlist_id', db.Integer,
        db.ForeignKey('playlists.id'),
        primary_key=True
    )
)

class Playlist(db.Model):
    __tablename__ = 'playlists'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    created_at = db.Column(
        db.DateTime,
        default = datetime.datetime.utcnow(),
        nullable=False
    )
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    song_id = db.relationship('songs', backref='playlists', lazy=True)
    followers = db.relationship(
        'users',
        secondary=users_playlists_table,
        lazy='subquery',
        backref=db.backref('playlists', lazy=True)
    )

    def __init__(self, name: str, created_at: datetime,):
        self.name = name
        self.created_at = created_at

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'song_id': self.song_id
        }
    

class Song(db.Model):
    __tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), nullable=False)
    date_released = db.Column(
        db.DateTime,
        nullable=True
    )
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'date_released': self.date_released.isoformat() if self.date_released else None,
            'playlist_id': self.playlist_id,
            'artist_id': self.artist_id
        }



class Artist(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    genre = db.Column(db.String(128), nullable=True)
    song_id = db.relationship('songs', backref='artists')


    def serialize(self):
        """ 
        :return: jsonified representation of the artist object
        """
        return {
            'id': self.id,
            'name': self.name,
            'genre': self.genre,
            'song_id': self.song_id
        }


