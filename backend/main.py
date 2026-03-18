from flask import Flask
from flask_cors import CORS
from routes.allroutes import allroute

app=Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(allroute)

if __name__ == "__main__" :
    app.run(port=8000,debug=True)