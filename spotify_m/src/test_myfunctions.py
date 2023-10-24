import pytest
import json
import requests
from datetime import datetime
from flask import Flask
from src import create_app, models
# from api import artists, playlists, songs, users

app = create_app()

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_user_route():
# Create a sample User for testing
    with app.app_context():
        existing_user = models.User.query.filter_by(username="Test User", password="Test Password").first()
        
        if not existing_user:
            user = models.User(username="Test User", password="Test Password")
            models.db.session.add(user)
            models.db.session.commit()
        else:
            user = existing_user

    client = app.test_client()

    response = client.get('/users')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1 
    assert data[0]['username'] == "Test User"

def test_artist_route():
    # Create a sample artist for testing
    with app.app_context():
        existing_artist = models.Artist.query.filter_by(name="Test Artist").first()
        
        if not existing_artist:
            artist = models.Artist(name="Test Artist")
            models.db.session.add(artist)
            models.db.session.commit()
        else:
            artist = existing_artist

    client = app.test_client()

    response = client.get('/artists')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1 # Verifies the artist sample created
    assert data[0]['name'] == "Test Artist"

def test_song_route():
    # Create a sample Song for testing
    with app.app_context():
        existing_song = models.Song.query.filter_by(title="Test Title").first()
        
        if not existing_song:
            song = models.Song(title="Test Title")
            models.db.session.add(song)
            models.db.session.commit()
        else:
            song = existing_song

    client = app.test_client()

    response = client.get('/songs')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1 
    assert data[0]['title'] == "Test Title"

def test_playlist_route():
    with app.app_context():
        existing_user = models.User.query.filter_by(username="Test User").first()
        
        if not existing_user:
            user = models.User(username="Test User", password="Test Password")
            models.db.session.add(user)
            models.db.session.commit()
        else:
            user = existing_user

        existing_song = models.Song.query.filter_by(title="Test Title").first()
        
        if not existing_song:
            song = models.Song(title="Test Title")
            models.db.session.add(song)
            models.db.session.commit()
        else:
            song = existing_song

        songs = [song]

        created_at = datetime(2023, 10, 25, 14, 30, 0)
        playlist = models.Playlist(name="Test Playlist", created_at=created_at, user_id=user.id)
        user.playlists.append(playlist)
        models.db.session.commit()

    client = app.test_client()

    response = client.get('/playlists')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['name'] == "Test Playlist"
    assert data[0]['created_at'] == created_at.isoformat()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)