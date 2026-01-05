import pytest
from werkzeug.exceptions import NotFound
from app.models.contact import Contact
from app.routes.contacts import get_contact_or_404
from app.extensions import db


def test_get_contact_or_404_exists(client, init_database) -> None:
    """Si el contacto existe, la función devuelve el objeto."""
    contact = Contact.query.first()  # obtenemos un contacto de init_database
    result = get_contact_or_404(contact.id)
    assert result.id == contact.id
    assert result.fullname == contact.fullname


def test_get_contact_or_404_not_found(client) -> None:
    """Si el contacto no existe, lanza abort(404)."""
    non_existing_id = 9999

    with pytest.raises(NotFound):
        get_contact_or_404(non_existing_id)
