from pyck.forms import Form
from wtforms import validators
from wtdojo import DojoStringField
from wtdojo.widgets import DojoTextArea


class ContactForm(Form):
    subject = DojoStringField('Subject', [validators.required("Subject cannot be empty")])
    email = DojoStringField('Email Address', [validators.Length(min=6, max=35),
                                              validators.Email(message="Invalid email format")])
    message = DojoStringField("Message", [validators.required("Message cannot be empty")],
                              widget=DojoTextArea())
