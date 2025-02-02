from datetime import datetime
from tkinter import W
from flask import Flask, make_response, render_template, sessions, url_for, flash, redirect, session
from markupsafe import Markup
from analyse import Analyse_Retro
import matplotlib.pyplot as plt

import numpy as np 
from analyse import Analyse_Retro
from calcul import prix

from forms import RegistrationForm, LoginForm
from datetime import datetime

import os

from pdf import pdf
from pricing import  total


#from pdf import pdf

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'



@app.route("/")
@app.route("/Accueil")
def Accueil():
    return render_template('Accueil.html')


@app.route("/index1")
def index1():
    return render_template('index1.html', title='contact')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.is_submitted():
        d1=datetime.strptime((form.date1.raw_data)[0], '%Y-%m-%d').date()
        print(d1)
        a=d1.strftime("%d/%m/%Y")
        
        x = total(form.ca.data, form.pivot.data, form.couts.data, a, form.ville.choices[int(form.ville.data)- 1][1])
        flash(f'La prime proposée est {x}', 'success')
        pdf(form.username.data, form.ville.choices[int(form.ville.data)- 1][1], d1, form.ca.data, form.pivot.data, form.couts.data, x)
        
        if form.submit1.data:
            path = form.username.data + '.pdf'
            os.system(path)
            # return render_template('about.html', title='About') 
    return render_template('devis.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    result = None
    if form.is_submitted():
        v=form.ville.choices[int(form.ville.data)-1][1]
        result = Analyse_Retro(v, form.ca.data, form.pivot.data, form.couts.data)
    
    return render_template('analyseRetro.html', title='retro', form=form, result=result)



if __name__ == '__main__':
    app.run(debug=True)