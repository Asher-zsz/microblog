from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Asher'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]

    return render_template("index.html", title = "Home", user = user , posts = posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit(): #get方法直接返回flase，若post方法，则检查所有attach validator的field，全对返回True，有错即返回false
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', form = form, title = 'Sign In') # form for login.html, title for base.html