from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# Flask Init
app = Flask(__name__)
app.env = 'development'  # development-production

# Mysql Connection
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1415'
app.config['MYSQL_DB'] = 'python'
mysql = MySQL(app)

# settings
app.secret_key = 'greenkey'
app.debug = True  # True-False


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', contacts=data)


@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname,email,phone) VALUES(%s, %s, %s);',
                    (fullname, email, phone))
        mysql.connection.commit()
        flash('contact added succesfully')
        cur.close()
    return redirect(url_for('index'))


@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE  FROM contacts WHERE id= (%s)', id)
    mysql.connection.commit()
    cur.close()
    flash('Contact deleted succesfully')
    return redirect(url_for('index'))


@app.route('/edit/<string:id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id={0}'.format(id))
    data = cur.fetchall()
    cur.close()
    return render_template('edit-contact.html', contact=data[0])


@app.route('/update/<string:id>', methods=['POST'])
def update(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE contacts SET fullname=%s, email=%s, phone=%s WHERE id=%s',
                    (fullname, email, phone, id))
        mysql.connection.commit()
        cur.close()
        flash('Contact Updated succesfully')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5500, )
