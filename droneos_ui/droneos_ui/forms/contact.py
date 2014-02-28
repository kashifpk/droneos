from pyck.forms import Form
from wtforms import TextField, TextAreaField, validators


class ContactForm(Form):
    subject = TextField('Subject', [validators.required("Subject cannot be empty")])
    email = TextField('Email Address', [validators.Length(min=6, max=35),
                                        validators.Email(message="Invalid email format")])
    message = TextAreaField("Message", [validators.required("Message cannot be empty")])
