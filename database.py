import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError

db_conn = os.environ['db_uri']

engine = create_engine(
  db_conn,
  connect_args={
    "ssl": {
      #insert ssl key here
      "ssl_ca": "/etc/ssl/cert.pem"
    }
  })


def load_movies():
  with engine.connect() as conn:
    movies = conn.execute(text("select * from movies"))
    #movies_dic= []

    movies_list = [dict(zip(movies.keys(), row)) for row in movies.fetchall()]
    return movies_list

  #print(movies_dic)


def get_movie_by_id(id):
  with engine.connect() as conn:
    #query = text("SELECT * FROM user_info WHERE email = :email")
    result = conn.execute(text("SELECT * FROM movies WHERE id = :id"),
                          {"id": id})

    result_list = [dict(zip(result.keys(), row)) for row in result.fetchall()]
    try:
      f_result = result_list[0]
      #print("DICTIONARY RESULT @#@@@##@##@##@#", result_list)
    except:
      return False
    if len(result_list) > 0:
      return f_result
    else:
      return False


def get_movie_by_name(name):
  with engine.connect() as conn:
    #query = text("SELECT * FROM user_info WHERE email = :email")
    result = conn.execute(
      text("SELECT * FROM movies WHERE movie_name = :name"), {"name": name})

    result_list = [dict(zip(result.keys(), row)) for row in result.fetchall()]
    try:
      f_result = result_list[0]
      #print("DICTIONARY RESULT @#@@@##@##@##@#", result_list)
    except:
      return False
    if len(result_list) > 0:
      return f_result
    else:
      return False


def insert_movie_info(movie_name, release_date, duration, blurb, poster_url, category, cast, genre, rating, summary, trailer):
  with engine.connect() as conn:
    try:
      conn.execute(
        text(
          "INSERT INTO movies (movie_name, release_date, duration, blurb, poster_url, category, cast, genre, rating, summary, trailer)  VALUES (:movie_name, :release_date, :duration, :blurb, :poster_url, :category, :cast, :genre, :rating, :summary, :trailer)"
        ), {
          "movie_name": movie_name,
          "release_date": release_date,
          "duration": duration,
          "blurb": blurb,
          "poster_url": poster_url,
          'category':category, 
          'cast':cast, 
          'genre':genre, 
          'rating':rating, 
          'summary':summary,
          'trailer':trailer
        })
      return True
    except IntegrityError:
      return False


def insert_user_info(username, email, password):
  with engine.connect() as conn:
    try:
      conn.execute(
        text(
          "INSERT INTO user_info (username, email, password, isConfirmed)  VALUES (:username, :email, :password, :confirmation)"
        ), {
          "username": username,
          "email": email,
          "password": password,        
          "confirmation": False
        })
      return True
    except IntegrityError:
      return False

def confirm_account(email):
  with engine.connect() as conn:
    conn.execute(
      text('UPDATE user_info SET isConfirmed = True where email = :email'), {
        "email": email
      }
    )

  
def get_user_by_email(email):
  with engine.connect() as conn:
    #query = text("SELECT * FROM user_info WHERE email = :email")
    result = conn.execute(text("SELECT * FROM user_info WHERE email = :email"),
                          {"email": email})

    result_list = [dict(zip(result.keys(), row)) for row in result.fetchall()]
    try:
      f_result = result_list[0]
      #print("DICTIONARY RESULT @#@@@##@##@##@#", result_list)
    except:
      return False
    if len(result_list) > 0:
      return f_result

    else:
      return False

def insert_payment_info(customer_id, ticket_name, ticket_amount, amount_paid, show_time, date, hall_name):
  with engine.connect() as conn:
    try:
      conn.execute(
        text(
          "INSERT INTO payment_info (customer_id, ticket_name, ticket_amount, amount_paid, show_time, date, payment_date_time, hall_name)  VALUES (:customer_id, :ticket_name, :ticket_amount, :amount_paid, :show_time, :date, NOW(), :hall_name)"
        ), {
          "customer_id": customer_id,
          "ticket_name": ticket_name,
          "ticket_amount": ticket_amount,
          "amount_paid": amount_paid,
          "show_time": show_time,
          "date": date,
          "hall_name": hall_name
        })
      return True
    except IntegrityError:
      return False

def get_movie_date_by_super_date(super_date):
  with engine.connect() as conn:
    result = conn.execute(
      text("SELECT date FROM movie_hall WHERE super_date = :super_date"), {"super_date": super_date})

    result_list = [dict(zip(result.keys(), row)) for row in result.fetchall()]
    try:
      f_result = result_list[0]
      #print("DICTIONARY RESULT @#@@@##@##@##@#", result_list)
    except:
      return False
    if len(result_list) > 0:
      return f_result
    else:
      return False

def get_show_info_movie_id(movie_id):
  with engine.connect() as conn:
    #query = text("SELECT * FROM user_info WHERE email = :email")
    result = conn.execute(text("select hall.hall_name, movies.movie_name, movie_hall.date, movie_hall.show_time, movie_hall.super_date from hall, movies, movie_hall where hall.id = movie_hall.hall_id and movies.id = movie_hall.movie_id and movies.id = :movie_id; "),
                          {"movie_id": movie_id})

  
    result_list = [dict(zip(result.keys(), row)) for row in result.fetchall()]
    return result_list
    '''try:
      f_result = result_list[0]
      #print("DICTIONARY RESULT @#@@@##@##@##@#", result_list)
    except:
      return False
    if len(result_list) > 0:
      return f_result
    else:
      return False'''

def get_user_purchase_by_user_id(user_id):
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM payment_info WHERE customer_id = :user_id"), {"user_id": user_id})

    result_list = [dict(zip(result.keys(), row)) for row in result.fetchall()]
    try:
      f_result = result_list
      #print("DICTIONARY RESULT @#@@@##@##@##@#", result_list)
    except:
      return False
    if len(result_list) > 0:
      return f_result
    else:
      return False

def reduce_hall_capacity_by_name(hall_name, quantity):
  with engine.connect() as conn:
    conn.execute(text("UPDATE hall SET capacity = capacity - :quantity WHERE hall_name = :hall_name;"),
                 { "quantity": quantity,
                   "hall_name": hall_name
                 })
    return True

def delete_user(email):
  with engine.connect() as conn:
    conn.execute(text("DELETE FROM user_info WHERE email = :email"),
                 {"email": email})


def delete_movie_from_db(movie_name):
  with engine.connect() as conn:
    conn.execute(text("DELETE FROM movies WHERE movie_name = :movie_name"),
                 {"movie_name": movie_name})
