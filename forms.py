from flask_wtf import Form
from wtforms import TextField, PasswordField, validators, SubmitField, IntegerField, BooleanField, SelectField


class AddForm(Form):
    firstname = TextField('First Name', [validators.Required()])
    middlename = TextField('Middle Name')
    lastname = TextField('Last Name', [validators.Required()])
    number = IntegerField('# of guests', [validators.Required()])
    submit_button = SubmitField('Submit')


class RegisterForm(Form):
    lastname = TextField('Last Name', [validators.Required()])
    invitecode = IntegerField('Invite Code', [validators.Required()])
    submit_button = SubmitField('Submit')


class RegisterFormVerify(Form):
    attending = SelectField('Will you be attending?', choices=[('False', 'No'),
                           ('True', 'Yes')])
    guests = SelectField('How many are attending?', coerce=int,
                         validators=[validators.optional()])
    submit_button = SubmitField('Submit')
