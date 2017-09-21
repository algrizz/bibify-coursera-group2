from flask import Flask, render_template, flash, request, session, redirect, url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

class NewMessage(Form):
    #Form used when registering
    TO = TextField('To:', validators=[validators.required()])
    SUBJECT = TextField('Title:', validators=[validators.required(), validators.Length(min=6, max=35)])
    MSG = TextField('Message:', validators=[validators.required(), validators.Length(min=1, max=200)])

    def reset(self):
        blankData = MultiDict([ ('csrf', self.reset_csrf() ) ])
        self.process(blankData)


class ReusableForm(Form):
    #Form used when registering
    name = TextField('Name:', validators=[validators.required()])
    email = TextField('Email:', validators=[validators.required(), validators.Length(min=6, max=35)])
    password = TextField('Password:', validators=[validators.required(), validators.Length(min=3, max=35)])
    password2 = TextField('Password2:', validators=[validators.required(), validators.Length(min=3, max=35)])
 
    def reset(self):
        blankData = MultiDict([ ('csrf', self.reset_csrf() ) ])
        self.process(blankData)

class LostPasswordForm(Form):
    #Form used only for password recovery / Asks email
    email = TextField('Email:', validators=[validators.required(), validators.Length(min=6, max=35)])

    def reset(self):
        blankData = MultiDict([ ('csrf', self.reset_csrf() ) ])
        self.process(blankData)

class EnterNewPassword(Form):
    #Form used only for password recovery / Asks password
    password = TextField('Password:', validators=[validators.required(), validators.Length(min=3, max=35)])

    def reset(self):
        blankData = MultiDict([ ('csrf', self.reset_csrf() ) ])
        self.process(blankData)

class LoginForm(Form):
    #Form used only for password recovery / Asks password
    email = TextField('Email:', validators=[validators.required(), validators.Length(min=6, max=35)])
    password = TextField('Password:', validators=[validators.required(), validators.Length(min=3, max=35)])

    def reset(self):
        blankData = MultiDict([ ('csrf', self.reset_csrf() ) ])
        self.process(blankData)

