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
        rule_list = reshuffle_list(rule_list)
    except:
        logger.critical("\"rule_list\" missing or not formatted properly")

    try:
        level_list = input_data["level_list"]
    except:
        logger.critical("\"level_list\" missing or not formatted properly")

    result = output.output(qc_data, rule_list, level_list)

    return jsonify(result)


def reshuffle_list(input_list):
    """
    Reorders the rule_list to match a set order
    """
    lookup_list = ["1-2s", "1-2.5s", "1-3s", "1-3.5s", "1-4s", "1-5s", "2-2s", "2/3-2s", "R-4s", "3-1s", "4-1s",
                   "7-T", "7-x", "8-x", "9-x", "10-x", "12-x"]

    # Filter the input_list to keep only values that are in the lookup list
    filtered_list = [item for item in input_list if item in lookup_list]

    # Sort the filtered_list based on the order in the lookup_list
    sorted_list = sorted(filtered_list, key=lambda x: lookup_list.index(x))

    return sorted_list


if __name__ == '__main__':
    # serve(app, host="0.0.0.0", port=5000)  # Production
    app.run(host='0.0.0.0', port=5000, debug=True)  # Development
