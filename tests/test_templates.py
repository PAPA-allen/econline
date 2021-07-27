import pytest
from app.extensions import db
from app.models import Admin
from flask import url_for

def test_index(app, captured_templates):
    response = app.test_client().get("/index")
    assert response.status_code == 200
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "home.html"

