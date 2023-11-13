import os
import requests
from flask import Flask, render_template, redirect, url_for, session, request
import ast
from flask_mail import Mail, Message
import random

from database import load_movies, insert_user_info, get_user_by_email, delete_user, get_movie_by_name, insert_movie_info, delete_movie_from_db, insert_payment_info, get_show_info_movie_id, get_movie_date_by_super_date, get_user_purchase_by_user_id, reduce_hall_capacity_by_name
from forms import SignupForm, LoginForm, updateMovieForm, deleteMovieForm  #import signupform func from forms.py
#from flask_login import UserMixin , login_user , LoginManager , login_required , logout_user , current_user
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
import stripe

app = Flask(__name__)

# app.config["MAIL_SERVER"] = 'smtp.gmail.com'
# app.config["MAIL_PORT"] = 465
# app.config["MAIL_USERNAME"] = 'ticketsystem0@gmail.com'
# app.config["MAIL_PASSWORD"] = os.environ['mail_pass']
# app.config["MAIL_USE_TLS"] = False
# app.config["MAIL_USE_SSL"] = True 

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.environ['secret_key']  #required for form validation

Session(app)

#public_key = "pk_test_6pRNASCoBOKtIshFeQd4XMUh"
stripe.api_key = os.environ['stripe_api_key']

app.config['WTF_CSRF_ENABLED'] = False

csrf = CSRFProtect(app)
mail = Mail(app)




@app.route('/')  #home
def home():
  card_data = load_movies()
  username = session.get('username')
  if username:
    print(username)
  return render_template('home.html', data=card_data, username=username)

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
  name = None
  form = SignupForm()

  if form.validate_on_submit():
    name = form.username.data
    email = form.email.data
    password1 = form.pass1.data
    password2 = form.pass2.data
    form.username.data = ''
    form.email.data = ''
    form.pass1.data = ''
    form.pass2.data = ''
    user = get_user_by_email(email)

    

    if user == False and insert_user_info(name, email, password1) and password1 == password2:
      print(f'Signup Succesful for {name} ')
      
      
      return redirect(url_for('signup_success', name=name))

    else:
      #flash('Username or email already exists!', 'danger')
      print("not successful")
  else:
    print(form.errors)

  return render_template('signup.html', name=name, form=form)
  
@app.route('/signup_success/<name>')
def signup_success(name):

  return render_template('signup_success.html', name=name, username = session.get('username'))


@app.route('/log_in', methods=['GET', 'POST'])
def log_in():
  form = LoginForm()
  if form.validate_on_submit():
    email = form.email.data
    password = form.password.data
    user = get_user_by_email(email)

    if user and user['password'] == password:
      session['user_id'] = user['id']
      session['username'] = user['username']
      print("login successfull")
      #print(session['username'])

      return redirect(url_for('home'))
    else:
      print("Invalid email or password!")

  return render_template('login.html', title='Log In', form=form)


@app.route('/log_out')
def log_out():
  # Remove the user's session data
  session.pop('username', None)
  session.pop('user_id', None)

  # Redirect the user to the home page
  return redirect(url_for('home'))


@app.route('/purchase_history')
def purchase_history():
  user_id = session.get('user_id')
  user_info = get_user_purchase_by_user_id(user_id)
  
  return render_template('purchase_history.html', user_info = user_info, username = session.get('username'))
  
@app.route('/checkout_2')
def checkout_2():
  movie = request.args.to_dict()
  #show_info = get_show_info_movie_id(movie["id"])
  show_time = request.args.get('show_time')
  hall_name = request.args.get('hall_name')
  super_date = request.args.get('super_date')
  date = get_movie_date_by_super_date(super_date)
  date = date["date"]
  #movie["show_time"] = "2PM"
  #movie["date"] = "2023-02-22"
  #movie["super_date"]  = "Thursday, 12 April 23"
  movie["hall_name"] = hall_name
  movie["show_time"] = show_time
  movie["date"] = date
  movie["super_date"]  = super_date
  return render_template('checkout_2.html', movie = movie, username = session.get('username'))


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
  #movie = ast.literal_eval(request.args.get('movie'))
  movie = request.args.to_dict()
  # use the file object in your product creation
  try:
    product = stripe.Product.create(
      name= movie["movie_name"],
      description= movie["genre"],
    )

    price = stripe.Price.create(
      unit_amount=469,
      currency="usd",
      product=product.id,
    )

    print("Product and price created successfully.")
  except stripe.error.InvalidRequestError as e:
    print(e)

  # Create a Checkout session using the Price object
  try:
    quantity = int(request.form['quantity'])
    movie["quantity"] = quantity
    checkout_session = stripe.checkout.Session.create(
      line_items=[
        {
          'price': price.id,
          'quantity': quantity,
          #'images': [product_image.id],
        },
      ],
      mode='payment',
      success_url=url_for('payment_success',_external=True, **movie),
      cancel_url=url_for('payment_failed', _external=True),
    )
  except Exception as e:
    return str(e)

  # Redirect the customer to the checkout page
  return redirect(checkout_session.url, code=303)


@app.route('/payment-success')
def payment_success():
    movie = request.args.to_dict()
    amount_paid = int(movie["quantity"]) * 500
    username = session.get('username')
    user_id = session.get('user_id')
  
    reduce_hall_capacity_by_name(movie["hall_name"], movie["quantity"])
    
    insert_payment_info(user_id, movie["movie_name"], int(movie["quantity"]), amount_paid, movie["show_time"], movie["date"], movie["hall_name"])
  
    return render_template('payment_success.html', username = username, movie = movie, amount_paid = amount_paid)

    

@app.route('/payment-failed')
def payment_failed():
    return render_template('payment_failed.html', username = session.get('username'))


#@app.route('/verify', methods=['POST'])
#def verify():
#  email = request.form['email']
#  verification_code = request.form['verification_code']
#  user = get_user_by_email(email)
#  if user['verification_code'] == verification_code:

#    return redirect(
#      url_for('signup_success', name=user['name'], email=user['email']))
#  else:
#    #flash('Invalid verification code!', 'danger')
#    delete_user(email)
#    return redirect(url_for('sign_up'))





@app.route('/shows')
def shows():
  # Fetch all movies from the database
  movies_list = load_movies()
  return render_template('shows.html', movies=movies_list, username = session.get('username'))


@app.route('/tickets')
def tickets():
  movie = request.args.to_dict()
  #movie = eval(movie)
  #poster_url = movie["poster_url"]
  show_info = get_show_info_movie_id(movie["id"])
  
  return render_template('tickets.html', show_info = show_info, movie=movie, username = session.get('username'))


@app.route('/user-profile')
def user_profile():
  return render_template('user-profile.html', username = session.get('username'))


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
  return log_in()


@app.route('/admin/update_movie', methods=['GET', 'POST'])
def update_movie():
  form = updateMovieForm()
  if form.validate_on_submit():
    movie_name = form.movie_name.data
    release_date = form.release_date.data
    duration = form.duration.data
    blurb = form.blurb.data
    poster_url = form.poster_url.data

    form.movie_name.data
    form.release_date.data
    form.duration.data
    form.blurb.data
    form.poster_url.data

    movie_exists = get_movie_by_name(movie_name)

    if movie_exists == False and insert_movie_info(
        movie_name, release_date, duration, blurb, poster_url):
      redirect(url_for('shows'))
  return render_template('update_movie.html', form=form)


@app.route('/admin/delete_movie', methods=['GET', 'POST'])
def delete_movie():
  form = deleteMovieForm()
  if form.validate_on_submit():
    movie_name = form.movie_name.data
    movie_exists = get_movie_by_name(movie_name)

    if movie_exists:
      delete_movie_from_db(movie_name)
      redirect(url_for('shows'))
  return render_template('delete_movie.html', form=form)


if __name__ == '__main__':
  app.run(host="0.0.0.0", debug=True)
