from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb
import pymysql
#import sshtunnel

app = Flask(__name__)
app.env = 'development'  # development-production
# Configuration de la base de datos

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1415'
app.config['MYSQL_DB'] = 'python'

mysql = MySQL(app)


app.debug = True  # True-False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname,email,phone) VALUES(%s, %s, %s)',
                    (fullname, email, phone))
        mysql.connection.commit()
        cur.close()
    return 'success'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5500, )
