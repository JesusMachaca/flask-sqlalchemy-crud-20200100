from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.contact import Contact
from utils.db import db

# Se crea un objeto Blueprint llamado "contacts" para agrupar rutas relacionadas con contactos
contacts = Blueprint("contacts", __name__)

# Ruta principal de la aplicación. Muestra todos los contactos almacenados en la base de datos.
# Renderiza la plantilla HTML "index.html" con los datos de los contactos.
@contacts.route('/')
def index():
    contacts = Contact.query.all() # Se consultan todos los contactos de la base de datos
    return render_template('index.html', contacts=contacts) # Se renderiza la plantilla HTML con los datos de los contactos

# Ruta para agregar un nuevo contacto a la base de datos
@contacts.route('/new', methods=['POST'])
def add_contact():
    if request.method == 'POST': # Si la petición es una POST (envío de datos del formulario)
        # Se obtienen los datos del formulario
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']

        # Se crea un nuevo objeto Contact con los datos del formulario
        new_contact = Contact(fullname, email, phone)

        # Se guarda el nuevo objeto Contact en la base de datos
        db.session.add(new_contact)
        db.session.commit()

        # Se muestra un mensaje de éxito al usuario utilizando el objeto flash
        flash('Contact added successfully!')

        # Se redirecciona al usuario a la página principal de la aplicación
        return redirect(url_for('contacts.index'))

# Ruta para actualizar los datos de un contacto existente
@contacts.route("/update/<string:id>", methods=["GET", "POST"])
def update(id):
    # Se consulta el contacto que se desea actualizar utilizando su ID
    contact = Contact.query.get(id)

    if request.method == "POST": # Si la petición es una POST (envío de datos del formulario)
        # Se actualizan los datos del contacto con los datos del formulario
        contact.fullname = request.form['fullname']
        contact.email = request.form['email']
        contact.phone = request.form['phone']

        # Se guarda el contacto actualizado en la base de datos
        db.session.commit()

        # Se muestra un mensaje de éxito al usuario utilizando el objeto flash
        flash('Contact updated successfully!')

        # Se redirecciona al usuario a la página principal de la aplicación
        return redirect(url_for('contacts.index'))

    # Se renderiza la plantilla HTML "update.html" con los datos del contacto a actualizar
    return render_template("update.html", contact=contact)

# Ruta para eliminar un contacto existente
@contacts.route("/delete/<id>", methods=["GET"])
def delete(id):
    # Se consulta el contacto que se desea eliminar utilizando su ID
    contact = Contact.query.get(id)

    # Se elimina el contacto de la base de datos
    db.session.delete(contact)
    db.session.commit()

    # Se muestra un mensaje de éxito al usuario utilizando el objeto flash
    flash('Contact deleted successfully!')

    # Se redirecciona al usuario a la página principal de la aplicación
    return redirect(url_for('contacts.index'))

# Ruta para mostrar información "Acerca de" la aplicación
@contacts.route("/about")
def about():
    return render_template("about.html") # Se renderiza la plantilla HTML "about.html"
