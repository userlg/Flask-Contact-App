from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from app.extensions import db
from app.models.contact import Contact

contacts_bp = Blueprint("contacts", __name__)

def get_contact_or_404(contact_id):
    contact = db.session.get(Contact, contact_id)
    if not contact:
        abort(404)
    return contact


@contacts_bp.route("/")
def index():
    contacts = db.session.execute(db.select(Contact)).scalars().all()
    return render_template("index.html", contacts=contacts)


@contacts_bp.route("/add_contact", methods=["POST"])
def add_contact():
    contact = Contact(
        fullname=request.form["fullname"],
        email=request.form["email"],
        phone=request.form["phone"],
    )
    db.session.add(contact)
    db.session.commit()
    flash("Contacto agregado correctamente")
    return redirect(url_for("contacts.index"))


@contacts_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_contact(id):
    contact =  contact = get_contact_or_404(id)

    if request.method == "POST":
        contact.fullname = request.form["fullname"]
        contact.email = request.form["email"]
        contact.phone = request.form["phone"]
        db.session.commit()
        flash("Contacto actualizado correctamente")
        return redirect(url_for("contacts.index"))

    return render_template("edit_contact.html", contact=contact)


@contacts_bp.route("/update/<int:id>", methods=["POST"])
def update_contact(id):
    contact = db.session.get(Contact, id)
    if not contact:
        abort(404)

    contact.fullname = request.form["fullname"]
    contact.email = request.form["email"]
    contact.phone = request.form["phone"]
    db.session.commit()
    flash("Contacto actualizado correctamente")
    return redirect(url_for("contacts.index"))


@contacts_bp.route("/delete/<int:id>")
def delete_contact(id):
    contact = db.session.get(Contact, id)
    if not contact:
        abort(404)

    db.session.delete(contact)
    db.session.commit()
    flash("Contacto eliminado")
    return redirect(url_for("contacts.index"))
