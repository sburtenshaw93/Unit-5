"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

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
    
    return render_template("all_movies_html", movies=movies)

@app.route("/movies/<movie_id>")
def show_movie(movie_id):
    
    movie = crud.get_movie_by_id(movie_id)
    
    return render_template("movie_details.html", movie=movie)

@app.route("/users", methods=["POST"])
def register_user():

    email = request.form.get("email")
    password = request.form.get("password")

    users = crud.get_users_by_email(email)
    if user:
        flash("Can't make an account with this email. Please try again.")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account has been sucessfully created")

    return redirect("/")

if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug = True, port = 5000, host = "localhost")
