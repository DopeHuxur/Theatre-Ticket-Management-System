from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email


class SignupForm(FlaskForm):
  username = StringField(label='Username', validators=[DataRequired()])
  email = StringField(label='Email', validators=[DataRequired(), Email()])
  pass1 = PasswordField(label='Password', validators=[DataRequired()])
  pass2 = PasswordField(label='Confirm Password', validators=[DataRequired()])
  submit = SubmitField(label='submit')


class LoginForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember_me = BooleanField('Remember me')
  submit = SubmitField('Log In')


class updateMovieForm(FlaskForm):
  movie_name = StringField(label='show_name', validators=[DataRequired()])
  release_date = StringField(label='release_date', validators=[DataRequired()])
  duration = StringField(label='duration', validators=[DataRequired()])
  blurb = StringField(label='blurb', validators=[DataRequired()])
  poster_url = StringField(label='poster_url', validators=[DataRequired()])
  category = StringField(label='category', validators=[DataRequired()])
  cast = StringField(label='cast', validators=[DataRequired()])
  genre = StringField(label='genre', validators=[DataRequired()])
  rating = StringField(label='rating', validators=[DataRequired()])
  summary = StringField(label='summary', validators=[DataRequired()])
  trailer = StringField(label='trailer', validators=[DataRequired()])

  Update = SubmitField('Update')


class deleteMovieForm(FlaskForm):
  movie_name = StringField(label='show_name', validators=[DataRequired()])
  Delete = SubmitField('Delete')
