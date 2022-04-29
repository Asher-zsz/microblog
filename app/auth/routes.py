from datetime import datetime
from flask import render_template, flash, redirect, url_for, request

from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User


from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from flask_babel import _

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit(): #get方法直接返回flase，若post方法，则检查所有attach validator的field，全对返回True，有错即返回false
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'))
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        # Right after the user is logged in by calling Flask-Login's login_user() function, 
        # the value of the next query string argument is obtained. 
        next_page = request.args.get('next') # request contains all the information that the client sent with the request
        if not next_page or url_parse(next_page).netloc != '': # 第二种情况，防止next变量中插入其他网站的绝对路径，进行恶意跳转
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', form = form, title = _('Sign In')) # form for login.html, title for base.html


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('Congratulations, you are now a registered user!'))
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title=_('Register'), form=form)
