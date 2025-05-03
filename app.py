from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize Flask application
app = Flask(__name__)

# Ensure the 'instance' folder exists for storing writable files like the database
os.makedirs(app.instance_path, exist_ok=True)

# Define the path to the SQLite database inside the instance folder
db_path = os.path.join(app.instance_path, "users.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

# Initialize the SQLAlchemy database connection
db = SQLAlchemy(app)

# Define the User model representing a table in the database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each user
    name = db.Column(db.String(100), nullable=False)  # User's name (required)
    role = db.Column(db.String(100), nullable=False)  # User's role (required)

# Create all database tables (if they don't exist yet)
with app.app_context():
    db.create_all()

# Define the main route to manage users
@app.route("/", methods=["GET", "POST"])
def manage_users():
    if request.method == "POST":
        # Get form data
        name = request.form["name"]
        role = request.form["role"]

        # Create new user and add to the database
        new_user = User(name=name, role=role)
        db.session.add(new_user)
        db.session.commit()

        # Redirect to the homepage to show updated user list
        return redirect(url_for("manage_users"))

    # For GET requests: query all users and render the template
    users = User.query.all()
    return render_template("users.html", users=users)

# Print the full database path to verify where it's being created
print("DB path:", os.path.abspath(app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", "")))

# Start the Flask development server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
