from flask import Flask
import export
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return json.dumps(export.run())

if __name__ == '__main__':
    app.run()