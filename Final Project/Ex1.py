"""app.py: the Flask backend. Run with:  python app.py"""
import os
from urllib.parse import quote

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

import helpers

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-only-change-me")

# Links to each site's own search page
SEARCH_LINKS = [
    {"name": "Handshake", "url": "https://app.joinhandshake.com/home"},
    {"name": "LinkedIn", "url": "https://www.linkedin.com/jobs/search/?keywords=business%20intern&location=Hawaii"},
    {"name": "Indeed", "url": "https://www.indeed.com/jobs?q=business+intern&l=Hawaii"},
]


# small helpers 

def get_users():
    return helpers.load_json(helpers.USERS_FILE, {})


def save_users(users):
    helpers.save_json(helpers.USERS_FILE, users)


def get_user():
    """The logged-in user's info (password hash, cart, likes), or None."""
    return get_users().get(session.get("email"))


@app.context_processor
def add_user_to_templates():
    """Gives every template: logged_in, cart, and likes."""
    user = get_user()
    return {
        "logged_in": user is not None,
        "cart": user["cart"] if user else [],
        "likes": user["likes"] if user else [],
    }


def saved_items(ids):
    """Internships whose id is in the list, soonest deadline first."""
    items = [helpers.add_status(i) for i in helpers.load_internships() if i["id"] in ids]
    items.sort(key=lambda i: (i["days_left"] < 0, i["deadline"]))
    return items


# browse page 

@app.route("/")
def home():
    internships = helpers.load_internships()

    # filters come from the URL, e.g. /?major=MIS&season=Summer
    filters = {}
    for name in ["source", "major", "season", "island", "company", "paid"]:
        filters[name] = request.args.get(name, "")
    filters["hide_passed"] = request.args.get("hide_passed") == "on"

    # dropdown choices = whatever values exist in the data
    options = {}
    for field in ["source", "major", "season", "island", "company"]:
        options[field] = sorted({i[field] for i in internships})

    results = helpers.filter_internships(internships, filters)
    return render_template("index.html", internships=results, filters=filters,
                           options=options, search_links=SEARCH_LINKS)


# cart and likes 

@app.route("/cart")
def cart_page():
    user = get_user()
    if user is None:
        return redirect(url_for("login"))
    items = saved_items(user["cart"])

    # Email: a mailto link that opens the user's email app with the list filled in
    lines = []
    for i in items:
        lines.append(f'{i["title"]} at {i["company"]} (apply by {i["deadline_pretty"]}): {i["url"]}')
    body = "My Hawaii internship shortlist:\n\n" + "\n".join(lines)
    subject = "My internship shortlist"
    mailto = f"mailto:{session['email']}?subject={quote(subject)}&body={quote(body)}"

    return render_template("saved.html", title="Your cart", items=items, mailto=mailto,
                           empty_text="Your cart is empty. Add internships you plan to apply for.")


@app.route("/liked")
def likes_page():
    user = get_user()
    if user is None:
        return redirect(url_for("login"))
    return render_template("saved.html", title="Liked internships", items=saved_items(user["likes"]),
                           mailto=None, empty_text="Nothing liked yet. Tap Like on any internship.")


@app.route("/cart/add/<int:internship_id>", methods=["POST"])
def add_to_cart(internship_id):
    users = get_users()
    email = session.get("email")
    if email not in users:
        return redirect(url_for("login"))
    if internship_id not in users[email]["cart"]:
        users[email]["cart"].append(internship_id)
    save_users(users)
    return redirect(request.referrer or url_for("home"))


@app.route("/cart/remove/<int:internship_id>", methods=["POST"])
def remove_from_cart(internship_id):
    users = get_users()
    email = session.get("email")
    if email not in users:
        return redirect(url_for("login"))
    if internship_id in users[email]["cart"]:
        users[email]["cart"].remove(internship_id)
    save_users(users)
    return redirect(request.referrer or url_for("home"))


@app.route("/like/<int:internship_id>", methods=["POST"])
def like(internship_id):
    users = get_users()
    email = session.get("email")
    if email not in users:
        return redirect(url_for("login"))
    liked = users[email]["likes"]
    if internship_id in liked:
        liked.remove(internship_id)   # clicking again un-likes
    else:
        liked.append(internship_id)
    save_users(users)
    return redirect(request.referrer or url_for("home"))


# ---------- accounts ----------

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        users = get_users()
        if "@" not in email or len(password) < 6:
            flash("Use a valid email and a password with at least 6 characters.")
        elif email in users:
            flash("That email already has an account. Try logging in.")
        else:
            users[email] = {"password_hash": generate_password_hash(password),
                            "cart": [], "likes": []}
            save_users(users)
            session["email"] = email
            return redirect(url_for("home"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        user = get_users().get(email)
        if user and check_password_hash(user["password_hash"], password):
            session["email"] = email
            return redirect(url_for("home"))
        flash("Email or password is incorrect.")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)