import pytest
from app import create_app, db
from app.models import User, Product
from werkzeug.security import generate_password_hash

@pytest.fixture
def app():
    # Use in-memory SQLite for testing
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
    })

    with app.app_context():
        # Drop any existing tables to start fresh
        db.drop_all()
        db.create_all()

        # Insert test users
        admin = User(username="admin", password=generate_password_hash("adminpass"), is_admin=True)
        user = User(username="user", password=generate_password_hash("userpass"), is_admin=False)
        db.session.add(admin)
        db.session.add(user)

        # Insert one test product
        product = Product(name="TestPhone", category="Phone", price=123.45, description="Test desc")
        db.session.add(product)

        db.session.commit()

    return app  # ✅ You need to return the app so the fixture works

@pytest.fixture
def client(app):
    return app.test_client()

def login(client, username, password):
    return client.post("/login", data={"username": username, "password": password}, follow_redirects=True)

def test_homepage_shows_products(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"TestPhone" in response.data

def test_search_returns_results(client):
    response = client.get("/search?q=test")
    assert response.status_code == 200
    assert b"TestPhone" in response.data

def test_non_admin_cannot_see_add_button(client):
    login(client, "user", "userpass")
    response = client.get("/")
    assert b"Add New Product" not in response.data

def test_admin_can_add_product(client, app):
    login(client, "admin", "adminpass")
    response = client.post("/add", data={
        "name": "NewItem",
        "category": "Gadget",
        "price": "9.99",
        "description": "A new item"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Product added!" in response.data
    with app.app_context():
        assert Product.query.filter_by(name="NewItem").first() is not None

def test_admin_can_edit_product(client, app):
    login(client, "admin", "adminpass")
    response = client.post("/edit/1", data={
        "name": "UpdatedPhone",
        "category": "Phone",
        "price": "199.99",
        "description": "Updated"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Product updated successfully." in response.data
    with app.app_context():
        assert Product.query.get(1).name == "UpdatedPhone"

def test_admin_can_delete_product(client, app):
    login(client, "admin", "adminpass")
    response = client.post("/delete/1", follow_redirects=True)
    assert response.status_code == 200
    assert b"Product deleted successfully." in response.data
    with app.app_context():
        assert Product.query.get(1) is None