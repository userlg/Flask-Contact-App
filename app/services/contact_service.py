from typing import List, Optional

from app.models.contact import Contact
from app.repositories.contact_repository import ContactRepository


class ContactService:
    """Service Layer Pattern para lógica de negocio de Contact."""

    def __init__(self, repository: ContactRepository = None):
        """Inicializa el servicio con un repositorio."""
        self.repository = repository or ContactRepository()

    def get_all_contacts(self) -> List[Contact]:
        """Obtiene todos los contactos."""
        return self.repository.get_all()

    def get_contact_by_id(self, contact_id: int) -> Optional[Contact]:
        """Obtiene un contacto por su ID."""
        return self.repository.get_by_id(contact_id)

    def create_contact(self, fullname: str, email: str, phone: str) -> Contact:
        """
        Crea un nuevo contacto con validaciones de negocio.
        
        Raises:
            ValueError: Si el email ya existe o los datos son inválidos.
        """
        # Validación de negocio: email único
        if self.repository.email_exists(email):
            raise ValueError("El email ya está registrado")

        # Validaciones adicionales
        if not fullname or not fullname.strip():
            raise ValueError("El nombre completo es requerido")

        if not email or not email.strip():
            raise ValueError("El email es requerido")

        if not phone or not phone.strip():
            raise ValueError("El teléfono es requerido")

        return self.repository.create(fullname.strip(), email.strip(), phone.strip())

    def update_contact(
        self, contact_id: int, fullname: str, email: str, phone: str
    ) -> Contact:
        """
        Actualiza un contacto existente con validaciones de negocio.
        
        Raises:
            ValueError: Si el contacto no existe o el email ya está en uso.
        """
        contact = self.repository.get_by_id(contact_id)
        if not contact:
            raise ValueError("Contacto no encontrado")

        # Validación: email único (excluyendo el contacto actual)
        if self.repository.email_exists(email, exclude_id=contact_id):
            raise ValueError("El email ya está registrado por otro contacto")

        # Validaciones adicionales
        if not fullname or not fullname.strip():
            raise ValueError("El nombre completo es requerido")

        if not email or not email.strip():
            raise ValueError("El email es requerido")

        if not phone or not phone.strip():
            raise ValueError("El teléfono es requerido")

        return self.repository.update(contact, fullname.strip(), email.strip(), phone.strip())

    def delete_contact(self, contact_id: int) -> None:
        """
        Elimina un contacto.
        
        Raises:
            ValueError: Si el contacto no existe.
        """
        contact = self.repository.get_by_id(contact_id)
        if not contact:
            raise ValueError("Contacto no encontrado")

        self.repository.delete(contact)
