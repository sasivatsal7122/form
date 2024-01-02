from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Regexp, Length, EqualTo

app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False

class LeadForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Regexp(r'^[a-zA-Z\s]+$', message='Only alphabets allowed')])
    email = StringField('Email', validators=[InputRequired(), Email()])
    phone_number = StringField('Phone Number (+91 not required)', validators=[InputRequired(), Regexp(r'^[0-9]{10}$', message='Invalid Indian phone number format')])
    password = PasswordField('Password (min 6 characters and max 12 characters)', validators=[
        InputRequired(),
        Regexp(r'^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,12}$', message='Invalid password format'),
        Length(min=6, max=12, message='Password must be at most 12 characters')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        InputRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Submit')

@app.route('/thank-you')
def thank_you():
    return "Thank you for your submission!"

@app.route('/', methods=['GET', 'POST'])
def lead_generation():
    form = LeadForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone_number = form.phone_number.data
        password = form.password.data
        print(f"Lead Information: Name: {name}, Email: {email}, Phone Number: {phone_number}, Password: {password}")
        return redirect(url_for('thank_you'))
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
