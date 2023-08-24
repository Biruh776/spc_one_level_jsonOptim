from flask import Flask, request, jsonify
import output
from waitress import serve
from logging_config import logger

# Create the Flask app
app = Flask(__name__)


@app.route('/spc', methods=['POST'])
def process_json():
    input_data = request.get_json()

    if not input_data:
        logger.critical(jsonify({'error': 'Invalid JSON data'}))

    try:
        qc_data = input_data["data"]
    except:
        logger.critical("\"data\" missing or not formatted properly")

    try:
        rule_list = input_data["rule_list"]
    except:
        logger.critical("\"rule_list\" missing or not formatted properly")

    result = output.output(qc_data, rule_list)

    return jsonify(result)


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5000)  # Production
    # app.run(host='0.0.0.0', port=5000, debug=True)  # Development
