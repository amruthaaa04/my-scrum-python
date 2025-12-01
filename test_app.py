from flask import Flask
app = Flask(__name__)
@app.route('/')
def index():
    return "hello from test server"
if __name__ == "__main__":
    app.run()
