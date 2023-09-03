from flask import Blueprint, render_template, redirect, url_for, request, \
    session, flash
from datetime import datetime
from .models import User, Movie, MovieSchema, Review, create_instance_from_json

from . import db
login_blueprint = Blueprint('login', __name__)
dashboard_blueprint = Blueprint('dashboard', __name__)
logout_blueprint = Blueprint('main', __name__)
movie_blueprint = Blueprint('movie', __name__)
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@login_blueprint.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()

        if not user:
            new_user = User(username=username)
            db.session.add(new_user)
            db.session.commit()
            session.update({"user": username})
            flash("You've been successfully registered", "success")
        else:
            session.update({"user": username})
            flash("You've been succesfully logged", "success")

    elif request.method == 'GET' and "user" not in session:
        return render_template("login.html")
    elif request.method == 'GET' and "user" in session:
        flash("Already logged in!", "warning")

    return redirect(url_for("dashboard.dashboard"))


@dashboard_blueprint.route('/dashboard')
def dashboard():
    if 'user' in session:
        username = session['user']

        movies = Movie.query.all()
        print("Movies:", movies)

        if request.method == "POST":
            user = User.query.filter_by(username=username).first()
            db.session.commit()
            days_registered = (datetime.utcnow() - user.registration_date).days
            return f'Hello, {user.username}. You' \
                   f're with us for {days_registered} days.'

        return render_template("dashboard.html", username=username, movies=movies)
    else:
        flash("You're not logged in!")

    return redirect(url_for("login.login"))


@dashboard_blueprint.route('/add_movie_review', methods=['POST'])
def add_movie_review():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        # Find the movie by title (assuming title is unique) or create a new one
        movie = Movie.query.filter_by(name=title).first()
        if movie is None:
            movie = Movie(name=title, content="")
            db.session.add(movie)
            db.session.commit()

        # Create a new review associated with the movie
        new_review = Review(content=content, movie_id=movie._id)

        # Add the review to the database
        db.session.add(new_review)
        db.session.commit()
        flash("Movie review added successfully", "success")

    return redirect(url_for("dashboard.dashboard"))


@logout_blueprint.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user', None)
        flash("You've been logged out!")
    else:
        flash("You're not logged in!")

    return redirect(url_for("login.login"))


def add_to_db(obj: Movie) -> None:
    db.session.add(obj)
    db.session.commit()


def delete_from_db(obj: Movie) -> None:
    db.session.delete(obj)
    db.session.commit()


@movie_blueprint.route('/movie', methods=['POST'])
def add_movie():
    body = request.json
    new_movie = create_instance_from_json(Movie, body)
    add_to_db(new_movie)

    return movie_schema.jsonify(new_movie)


@movie_blueprint.route('/movie', methods=['GET'])
def get_movies():
    all_movies = Movie.query.all()

    return movies_schema.jsonify(all_movies)


@movie_blueprint.route('/movie/<int:id>', methods=['GET'])
def get_movie_by_id(id: int):
    found_movie = Movie.query.get(id)

    return movie_schema.jsonify(found_movie)


@movie_blueprint.route('/movie/<int:id>', methods=['DELETE'])
def delete_movie_by_id(id: int):
    found_movie = Movie.query.get(id)
    delete_from_db(found_movie)

    return movie_schema.jsonify(found_movie)


@movie_blueprint.route('/movie/<int:id>', methods=['PUT'])
def modify_movie_by_id(id: int):
    found_movie = Movie.query.get(id)
    body = request.json
    temp = create_instance_from_json(Movie, body)
    found_movie.update(temp)
    db.session.commit()
    return movie_schema.jsonify(found_movie)
