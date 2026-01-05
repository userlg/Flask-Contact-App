from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from app.forms.contact_form import ContactForm
from app.services.contact_service import ContactService

contacts_bp = Blueprint("contacts", __name__)
contact_service = ContactService()


def get_contact_or_404(contact_id):
    """Helper function para obtener contacto o lanzar 404."""
    contact = contact_service.get_contact_by_id(contact_id)
    if not contact:
        abort(404)
    return contact


@contacts_bp.route("/")
def index():
    """Lista todos los contactos."""
    contacts = contact_service.get_all_contacts()
    form = ContactForm()  # Formulario para agregar nuevo contacto
    return render_template("index.html", contacts=contacts, form=form)


@contacts_bp.route("/add_contact", methods=["POST"])
def add_contact():
    """Crea un nuevo contacto."""
    form = ContactForm()
    
    if form.validate_on_submit():
        try:
            contact_service.create_contact(
                fullname=form.fullname.data,
                email=form.email.data,
                phone=form.phone.data,
            )
            flash("Contacto agregado correctamente", "success")
        except ValueError as e:
            flash(str(e), "error")
    else:
        # Mostrar errores de validación
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{getattr(form, field).label.text}: {error}", "error")
    
    return redirect(url_for("contacts.index"))


@contacts_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_contact(id):
    """Edita un contacto existente."""
    contact = get_contact_or_404(id)
    form = ContactForm(obj=contact)  # Pre-llenar formulario con datos del contacto

    if request.method == "POST" and form.validate_on_submit():
        try:
            contact_service.update_contact(
                contact_id=id,
                fullname=form.fullname.data,
                email=form.email.data,
                phone=form.phone.data,
            )
            flash("Contacto actualizado correctamente", "success")
            return redirect(url_for("contacts.index"))
        except ValueError as e:
            flash(str(e), "error")

    return render_template("edit_contact.html", contact=contact, form=form)


@contacts_bp.route("/delete/<int:id>")
def delete_contact(id):
    """Elimina un contacto."""
    try:
        contact_service.delete_contact(id)
        flash("Contacto eliminado correctamente", "success")
    except ValueError as e:
        flash(str(e), "error")
    
    return redirect(url_for("contacts.index"))
