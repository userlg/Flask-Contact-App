import pytest
from app import create_app
from app.extensions import db as _db
from app.models.contact import Contact


@pytest.fixture(scope="module")
def app():
    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",  # base de datos en memoria
        WTF_CSRF_ENABLED=False,
    )

    with app.app_context():
        _db.create_all()  # crear tablas
        yield app
        _db.drop_all()  # limpiar al finalizar


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()


@pytest.fixture(scope="function")
def init_database(app):
    # Esta fixture puede pre-cargar datos si quieres
    contact = Contact(fullname="Test User", email="test@example.com", phone="123456789")
    _db.session.add(contact)
    _db.session.commit()
    yield _db  # retorna la db con los datos
    _db.session.remove()
    _db.drop_all()
    _db.create_all()
