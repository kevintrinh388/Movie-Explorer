# pylint: disable=no-member, invalid-envvar-default, redefined-outer-name
"""
App will have a homepage that displays information for a random movie
"""
import random
import os
import flask
from flask_login import LoginManager, current_user, login_required, logout_user
import flask_login
from models import db, Username, Comment
from tmdb import fetch_movie
from wiki import fetch_wiki


app = flask.Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# set up a separate route to serve the index.html file generated
# by create-react-app/npm run build.
# By doing this, we make it so you can paste in all your old app routes
# from Milestone 2 without interfering with the functionality here.
bp = flask.Blueprint(
    "bp",
    __name__,
    template_folder="./static/react",
)

login_manager = LoginManager()
login_manager.init_app(app)


# Point SQLAlchemy to your Heroku database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("MY_DATABASE_URL")
# Gets rid of a warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    """
    Required by flask_login
    """
    return Username.query.get(int(user_id))


# route for serving React page
@bp.route("/reviews")
def reviews():
    """
    Reviews page
    """
    # NB: DO NOT add an "index.html" file in your normal templates folder
    # Flask will stop serving this React page correctly
    return flask.render_template("index.html")


@app.route("/")
def index():
    """
    App start
    """

    return flask.redirect(flask.url_for("login"))


@login_required
@app.route("/home", methods=["GET", "POST"])
def home():
    """
    Home page
    """

    current_username = current_user.username

    if flask.request.method == "POST":
        data = flask.request.form
        rating = data["rating"]
        comment = data["comment"]
        movie = data["movie"]

        new_comment = Comment(
            rating=rating, comment=comment, movie=movie, username=current_username
        )
        db.session.add(new_comment)
        db.session.commit()

        return flask.redirect(flask.url_for("home"))

    movies = [5174, 379686, 447404, 768744, 16859]
    chosen = random.choice(movies)
    details = fetch_movie(chosen)
    wiki = fetch_wiki(details["title"])

    reviews = Comment.query.filter_by(movie=chosen).all()

    return flask.render_template(
        "home.html",
        current_username=current_username,
        details=details,
        wiki=wiki,
        movie=chosen,
        reviews=reviews,
    )


@login_required
@app.route("/get_reviews")
def get_reviews():
    """
    Get user's reviews
    """
    user_reviews = Comment.query.filter_by(username=current_user.username).all()

    list_reviews = []

    for i in user_reviews:
        review_to_add = {
            "id": i.id,
            "movie": i.movie,
            "rating": i.rating,
            "comment": i.comment,
        }
        list_reviews.append(review_to_add)

    return flask.jsonify(list_reviews)


@app.route("/delete_reviews", methods=["POST"])
def delete_reviews():
    """
    Deletes reviews chosen by user
    """
    reviews = list(flask.request.get_json(force=True))

    if len(reviews) == 0:
        return flask.jsonify({"SUCCESS": "FALSE"})

    for review in reviews:
        Comment.query.filter_by(id=review["id"]).delete()
        db.session.commit()

    return flask.jsonify({"SUCCESS": "TRUE"})


@app.route("/edit_reviews", methods=["POST"])
def edit_reviews():
    """
    Edits reviews changed by user
    """
    reviews = list(flask.request.get_json(force=True))
    if len(reviews) == 0:
        return flask.jsonify({"SUCCESS": "FALSE"})

    for review in reviews:

        Comment.query.filter_by(id=review["id"]).update(
            {"comment": review["comment"], "rating": review["rating"]},
        )
        db.session.commit()

    return flask.jsonify({"SUCCESS": "TRUE"})


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """
    signup page
    """
    if flask.request.method == "POST":
        data = flask.request.form
        signup_name = data["username"]
        new_username = Username(username=signup_name)
        # if username exists, redirect back to signup
        if len(Username.query.filter_by(username=signup_name).all()) != 0:
            flask.flash("Username already exists")
            return flask.redirect(flask.url_for("signup"))
        # else add it to database
        db.session.add(new_username)
        db.session.commit()
        flask.flash("Signup successful!")
        return flask.redirect(flask.url_for("login"))

    return flask.render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    login page
    """
    if flask.request.method == "POST":
        data = flask.request.form
        login_name = data["username"]
        # if username exists go to home page
        if len(Username.query.filter_by(username=login_name).all()) != 0:
            user = Username.query.filter_by(username=login_name).first()
            flask_login.login_user(user)
            return flask.redirect(flask.url_for("home"))
        # else redirect to login page again
        flask.flash("Username does not exist")
        return flask.redirect(flask.url_for("login"))

    return flask.render_template("login.html")


@login_required
@app.route("/signout", methods=["GET", "POST"])
def signout():
    """
    signout user
    """
    logout_user()
    return flask.redirect(flask.url_for("login"))


app.register_blueprint(bp)

app.run(
    debug=True,
    host="0.0.0.0",
    port=int(os.getenv("PORT", 8080)),
)
