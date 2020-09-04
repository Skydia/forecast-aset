from app import app
from flask import Flask, render_template

import forms

@app.route('/')
def index():
    return render_template('index.html', variabel_bebas='custom variable')

@app.route('/about', methods=['GET','POST'])
def about():
    form = forms.AddTaskForm()
    if form.validate_on_submit():
        print('Submitted', form.title.data)
    return render_template('about.html', variabel_bebas='custom variable', form=form)