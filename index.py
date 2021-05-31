from flask import Flask, render_template,redirect,url_for


app = Flask(__name__)
app.env = 'development'


# app.debug = 'on'

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/contact')
def contact():
    return 'This is a contact route'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5500, )
