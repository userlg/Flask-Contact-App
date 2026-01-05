from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, Length, Regexp


class ContactForm(FlaskForm):
    """Formulario de validación para Contact usando WTForms."""

    fullname = StringField(
        "Nombre Completo",
        validators=[
            DataRequired(message="El nombre completo es requerido"),
            Length(max=100, message="El nombre no puede exceder 100 caracteres"),
        ],
        render_kw={"placeholder": "Ej: Juan Pérez", "class": "form-control"},
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(message="El email es requerido"),
            Email(message="Debe ser un email válido"),
            Length(max=120, message="El email no puede exceder 120 caracteres"),
        ],
        render_kw={"placeholder": "Ej: juan@example.com", "class": "form-control", "type": "email"},
    )

    phone = StringField(
        "Teléfono",
        validators=[
            DataRequired(message="El teléfono es requerido"),
            Length(max=20, message="El teléfono no puede exceder 20 caracteres"),
            Regexp(
                r"^[\d\s\-\+\(\)]+$",
                message="El teléfono solo puede contener números, espacios, guiones y paréntesis",
            ),
        ],
        render_kw={"placeholder": "Ej: +34 123 456 789", "class": "form-control", "type": "tel"},
    )
