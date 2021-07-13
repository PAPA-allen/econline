def test_home(client):
    response = client.get("/")
    assert response.status_code == 200


def test_thank_you(client):
    response = client.get("/thank-you")
    assert response.status_code == 200


def test_error_page(client):
    response = client.get("/error")
    assert response.status_code == 200


def test_contact_page(client):
    response = client.get("/contact-us")
    assert response.status_code == 200