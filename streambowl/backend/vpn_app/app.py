#!/usr/bin/python3
import json
from flask import request
from flask import Flask
from extract import ExtractHtml

app = Flask(__name__)
base_obj = ExtractHtml()

@app.route('/get_html_content', methods=['GET', 'POST'])
def get_html_content():
    data = request.get_data()
    jdata = json.loads(data)
    content = base_obj.page_getter(url_link=jdata['url'])
    response = app.response_class(
        status=200,
        response = content,
        mimetype='application/json'
    )
    return response

@app.route('/health_status', methods=['GET', 'POST'])
def health_monitoring():
    data = base_obj.health_check()
    return app.response_class(response=json.dumps(data), status=200, mimetype='application/json')

if __name__ == "__main__":
    app.run(debug=True, port=5555, host="0.0.0.0",)
