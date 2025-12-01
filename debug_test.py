from flask import Flask
from flask_login import LoginManager, UserMixin, login_user, current_user

app = Flask(__name__)
app.secret_key = "testsecret"

login_manager = LoginManager(app)

class User(UserMixin):
    def __init__(self, id, first_name, last_name):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

@login_manager.user_loader
def load_user(user_id):
    return User(1, "John", "Doe") if user_id == "1" else None

@app.route("/")
def root():
    return "Root OK - go to /login or /debug"

@app.route("/login")
def login():
    test_user = User(1, "John", "Doe")
    login_user(test_user)
    return "Logged in as: " + test_user.full_name

@app.route("/debug")
def debug():
    if current_user.is_authenticated:
        return "Current user full_name: " + current_user.full_name
    return "Not logged in."

if __name__ == "__main__":
    # show all logs on console and listen only on localhost
    app.run(host="127.0.0.1", port=5000, debug=True)
