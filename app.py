from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dhOI@hd02d@4f28864f4f29D'

from routes import *


if (__name__ == '__main__'):
    app.run(debug=True)