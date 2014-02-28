from pyck.forms import Form
from wtforms import validators, widgets
from wtforms.fields import (PasswordField, TextField, DateField, TextAreaField, RadioField,
                            BooleanField, SelectField, SelectMultipleField)


class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(html_tag='ul', prefix_label=False)
    option_widget = widgets.CheckboxInput()


class UserForm(Form):

    user_id = TextField('User ID', [validators.required()])
    password = PasswordField('Password', [validators.required(),
                                          validators.EqualTo('verify_password', 'Passwords must match')])
    verify_password = PasswordField('Verify Password', [validators.required()])


class LoginForm(Form):

    user_id = TextField('User ID', [validators.required()])
    password = PasswordField('Password', [validators.required()])


class PermissionForm(Form):

    permission = TextField('Permission', [validators.required()])
    description = TextField('Description')


class RoutePermissionForm(Form):

    route_name = SelectField("Route", [validators.required()])
    request_methods = MultiCheckboxField("Request Methods", choices=[('ALL', 'ALL'),
                                                                     ('GET', 'GET'), ('POST', 'POST'),
                                                                     ('PUT', 'PUT'), ('DELETE', 'DELETE'),
                                                                     ('HEAD', 'HEAD'), ('OPTIONS', 'OPTIONS')])
    permissions = MultiCheckboxField("Permissions")


__all__ = ['UserForm', 'PermissionForm', 'RoutePermissionForm', 'LoginForm']
