"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
import os

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# Replace this with routes and view functions!

@app.route('/')
def homepage():
    
    return render_template('homepage.html')

@app.route("/movies")
def allmovies():
    
    movies = crud.get_movies()
    
    return render_template("all_movies.html", movies=movies)

@app.route("/users")
def all_users():
    
    users = crud.get_users()
    
    return render_template("all_users.html", users=users)

@app.route("/movies/<movie_id>")
def show_movie(movie_id):
    
    movie = crud.get_movie_by_id(movie_id)
    
    return render_template("movie_details.html", movie=movie)

@app.route("/users/<user_id>")
def user_list(user_id):
     user = crud.get_user_by_id(user_id)
     
     return render_template("user_details.html", user=user)

@app.route("/users", methods=["POST"])
def register_user():

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash("Can't make an account with this email. Please try again.")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account has been sucessfully created")

    return redirect("/")

@app.route("/login", methods=["POST"])
def process_login():
    
    email = request.form.get("email")
    password = request.form.get("password")
    
    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect")
    else:
        session["user_email"] = user.email
        flash(f"Successfully Logged in")
    return redirect("/")    

@app.route("/movies/<movie_id>/ratings", methods=["POST"])
def create_rating(movie_id):

    logged_in_email = session.get("user_email")
    rating_score = request.form.get("user_email")
    
    if logged_in_email is None:
        flash("Please login to rate this movie.")
    elif not rating_score:
        flash("Error, Select a vaild rating.")
    else:
        user = crud.get_user_by_email(logged_in_email)
        movie = crud.get_movie_by_id(movie_id)

        rating = crud.create_rating(user, movie, int(rating_score))
        db.session.add(rating)
        db.session.commit()

        flash(f"You rated this movie {rating_score} out of 5.")

    return redirect(f"/movies/{movie_id}")

@app.route("/update_rating", methods=["POST"])
def update_rating():
    rating_id = request.json["rating_id"]
    updated_score = request.json["updated_score"]
    crud.update_rating(rating_id, updated_score)
    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app, db_uri=os.environ['POSTGRES_URI'])
    app.run(debug = True, port = 5000, host = "localhost")
