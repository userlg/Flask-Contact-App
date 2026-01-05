from app.extensions import db
from app.models.contact import Contact


def test_index_page(client, init_database) -> None:
    """Test que la página principal carga correctamente y muestra contactos"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Test User" in response.data  # verifica que aparece el contacto agregado


def test_add_contact(client) -> None:
    """Test agregar un nuevo contacto"""
    response = client.post(
        "/add_contact",
        data={
            "fullname": "John Doe",
            "email": "john@example.com",
            "phone": "987654321",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Contacto agregado correctamente" in response.data
    assert b"John Doe" in response.data


def test_edit_contact(client, init_database) -> None:
    """Test editar un contacto existente"""
    # Obtenemos el ID del contacto agregado por init_database
    from app.models.contact import Contact

    contact = Contact.query.first()

    response = client.post(
        f"/edit/{contact.id}",
        data={
            "fullname": "Updated Name",
            "email": contact.email,
            "phone": contact.phone,
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Contacto actualizado correctamente" in response.data
    assert b"Updated Name" in response.data


def test_delete_contact(client) -> None:
    # Crear un contacto de prueba
    contact = Contact(fullname="Test", email="test@test.com", phone="12345")
    db.session.add(contact)
    db.session.commit()

    # Llamar al endpoint delete
    client.get(f"/delete/{contact.id}")

    # Usar db.session.get para evitar warnings
    deleted_contact = db.session.get(Contact, contact.id)
    assert deleted_contact is None


def test_edit_contact_get_not_found(client) -> None:
    # Un ID que seguramente no existe
    non_existing_id = 9999

    # Hacemos GET a la ruta edit
    response = client.get(f"/edit/{non_existing_id}")

    # Comprobamos que devuelve 404
    assert response.status_code == 404


def test_edit_contact_post_not_found(client) -> None:
    non_existing_id = 9999

    response = client.post(
        f"/edit/{non_existing_id}",
        data={
            "fullname": "Should Fail",
            "email": "fail@test.com",
            "phone": "000000",
        },
    )

    assert response.status_code == 404


def test_update_contact_not_found(client):
    non_existing_id = 9999

    response = client.post(
        f"/update/{non_existing_id}",
        data={"fullname": "No Name", "email": "noemail@test.com", "phone": "000000"},
    )

    assert response.status_code == 404


def test_delete_contact_not_found(client):
    non_existing_id = 9999

    response = client.get(f"/delete/{non_existing_id}")

    assert response.status_code == 404
