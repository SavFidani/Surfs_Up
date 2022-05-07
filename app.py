from flask import Flask

# Create the flask app instance
app = Flask(__name__)

# Create the first route
@app.route('/')
def hello_world():
    return 'Hello world'

