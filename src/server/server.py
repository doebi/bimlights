from flask import Flask
import lf

app = Flask(__name__)

@app.route("/")
def hello():
    return lf.buildData()

if __name__ == "__main__":
    app.run(host='0.0.0.0')
