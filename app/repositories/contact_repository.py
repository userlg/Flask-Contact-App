from typing import List, Optional

from app.extensions import db
from app.models.contact import Contact


class ContactRepository:
    """Repository Pattern para manejar operaciones de base de datos de Contact."""

    @staticmethod
    def get_all() -> List[Contact]:
        """Obtiene todos los contactos."""
        return db.session.execute(db.select(Contact)).scalars().all()

    @staticmethod
    def get_by_id(contact_id: int) -> Optional[Contact]:
        """Obtiene un contacto por su ID."""
        return db.session.get(Contact, contact_id)

    @staticmethod
    def create(fullname: str, email: str, phone: str) -> Contact:
        """Crea un nuevo contacto."""
        contact = Contact(fullname=fullname, email=email, phone=phone)
        db.session.add(contact)
        db.session.commit()
        return contact

    @staticmethod
    def update(contact: Contact, fullname: str, email: str, phone: str) -> Contact:
        """Actualiza un contacto existente."""
        contact.fullname = fullname
        contact.email = email
        contact.phone = phone
        db.session.commit()
        return contact

    @staticmethod
    def delete(contact: Contact) -> None:
        """Elimina un contacto."""
        db.session.delete(contact)
        db.session.commit()

    @staticmethod
    def email_exists(email: str, exclude_id: Optional[int] = None) -> bool:
        """Verifica si un email ya existe en la base de datos."""
        query = db.select(Contact).where(Contact.email == email)
        if exclude_id:
            query = query.where(Contact.id != exclude_id)
        result = db.session.execute(query).scalar_one_or_none()
        return result is not None
