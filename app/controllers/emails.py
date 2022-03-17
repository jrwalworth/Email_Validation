from flask import Flask, session, render_template, redirect, request, flash
from app import app
from app.models.email import Email

#home
@app.route('/')
def index():
    return render_template('index.html')

#hidden route to validate email before submitting to DB
@app.route('/add_email', methods=['POST'])
def insert():
    data = {
        'email' : request.form['email']
    }
    if not Email.validate_email(request.form):
        return redirect('/')
    Email.insert(data)
    flash(f'Success! Email {data} has been added to the database.')
    return redirect('/success')

#success page
@app.route('/success', methods=['GET'])
def success():
    return render_template('success.html', emails = Email.get_all())

#delete email
@app.route('/delete/<email>')
def destroy(email):
    data = {
        'email': email
    }
    Email.delete(data)
    flash(f'Email {data} successfully deleted from the database.')
    return redirect('/success')