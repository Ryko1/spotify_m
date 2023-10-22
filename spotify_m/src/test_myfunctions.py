import pytest
import json
from flask import Flask
from src import create_app, models
# from api import artists, playlists, songs, users

app = create_app()

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_artist_route():
    # Create a sample artist for testing
    with app.app_context():
        artist = models.Artist(name="Test Artist")
        models.db.session.add(artist)
        models.db.session.commit()

    client = app.test_client()

    response = client.get('/artists')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1 # Verifies the artist sample created
    assert data[0]['name'] == "Test Artist"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)