from app.models import User

from flask import request
from flask_wtf import FlaskForm # flask_wt提供了使用flask写WTForm的接口
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length
from flask_babel import _, lazy_gettext as _l


class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About me'), validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Oops, this one has been taken.'))

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    post = TextAreaField(_l('Say something'), validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField(_l('Submit'))

class SearchForm(FlaskForm):
    q = StringField(_l('Search'), validators=[DataRequired()])
    # For a form that has a text field, the browser will submit the form when you press Enter with the focus on the field, so a button is not needed.
    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args # request.args for GRT method, while request.form for POST, here we use GET.
        if 'meta' not in kwargs:
            kwargs['meta'] = {'csrf': False} # bypass CSRF validation for this form
        super(SearchForm, self).__init__(*args, **kwargs)
