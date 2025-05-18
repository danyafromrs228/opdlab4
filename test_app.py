import pytest
from io import BytesIO
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):

    response = client.get('/')
    assert response.status_code == 200
    assert 'text/html' in response.content_type
    assert len(response.data) > 0
def test_file_upload(client):

    test_content = "hello world hello python hello flask"
    test_file = (BytesIO(test_content.encode('utf-8')), 'test.txt')
    response = client.post(
        '/upload',
        data={'file': test_file},
        content_type='multipart/form-data'
    )

    assert response.status_code == 200
    response_text = response.data.decode('utf-8')
    assert 'hello' in response_text.lower()
    assert '3' in response_text

def test_empty_file(client):
    test_file = (BytesIO(b''), 'empty.txt')
    response = client.post(
        '/upload',
        data={'file': test_file},
        content_type='multipart/form-data'
    )
    assert response.status_code == 200
    assert 'не содержит слов' in response.data.decode('utf-8').lower()
