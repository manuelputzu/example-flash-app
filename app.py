from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Start with a list of users
user_list = [
    {"id": 1, "name": "Rosa", "role": "Admin"},
    {"id": 2, "name": "Romeo", "role": "Member"},
    {"id": 3, "name": "Anna", "role": "Guest"},
]

@app.route("/", methods=["GET", "POST"])
def manage_users():
    if request.method == "POST":
        name = request.form.get("name")
        role = request.form.get("role")
        new_id = len(user_list) + 1

        new_user = {"id": new_id, "name": name, "role": role}
        user_list.append(new_user)

        return redirect(url_for("manage_users"))

    return render_template("users.html", users=user_list)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)