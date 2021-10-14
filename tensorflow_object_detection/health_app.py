from flask import Flask

app = Flask(__name__)

@app.route('/healthcheck', methods=['GET', 'POST'])
def healthcheck():
    return "success"

if __name__ == "__main__":
    app.run(debug=False, port=5000, host="0.0.0.0",)