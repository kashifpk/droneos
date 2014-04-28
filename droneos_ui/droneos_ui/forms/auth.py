from pyck.forms import Form
from wtforms import validators, widgets
from wtforms.fields import (PasswordField, TextField, DateField, TextAreaField, RadioField,
                            BooleanField, SelectField, SelectMultipleField)
from wtdojo import DojoStringField, DojoSelectField
from wtdojo.widgets import DojoTextArea, DojoCheckBox, DojoPasswordBox


class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(html_tag='ul', prefix_label=False)
    option_widget = DojoCheckBox()


class UserForm(Form):

    user_id = DojoStringField('User ID', [validators.required()])
    password = DojoStringField('Password', [validators.required(),
                                            validators.EqualTo('verify_password', 'Passwords must match')],
                               widget=DojoPasswordBox())
    verify_password = DojoStringField('Verify Password', [validators.required()], widget=DojoPasswordBox())


class LoginForm(Form):

    user_id = DojoStringField('User ID', [validators.required()])
    password = DojoStringField('Password', [validators.required()], widget=DojoPasswordBox())


class PermissionForm(Form):

    permission = DojoStringField('Permission', [validators.required()])
    description = DojoStringField('Description')


class RoutePermissionForm(Form):

    route_name = DojoSelectField("Route", [validators.required()])
    request_methods = MultiCheckboxField("Request Methods", choices=[('ALL', 'ALL'),
                                                                     ('GET', 'GET'), ('POST', 'POST'),
                                                                     ('PUT', 'PUT'), ('DELETE', 'DELETE'),
                                                                     ('HEAD', 'HEAD'), ('OPTIONS', 'OPTIONS')])
    permissions = MultiCheckboxField("Permissions")


__all__ = ['UserForm', 'PermissionForm', 'RoutePermissionForm', 'LoginForm']
