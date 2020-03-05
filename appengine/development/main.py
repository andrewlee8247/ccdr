from flask import Flask, jsonify, request
from google.cloud import storage
import pandas as pd
from io import BytesIO
from ccdr_lib import predictions
from flasgger import Swagger


app = Flask(__name__)
Swagger(app)
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


@app.route('/')
def home():
    """Returns home page HTML"""
    return """
    <!DOCTYPE html>
    <head>
    <title>Credit Card Default Risk App</title>
    <style>
    .content{
        max-width: 500px;
        margin: auto;
    }
    .button {
        background-color: #4CAF50;
        border: none;
        color: white;
        padding: 15px 25px;
        text-align: center;
        font-size: 16px;
        cursor: pointer;
    }
    .button:hover {
        background-color: green;
    }
    </style>
    </head>
    <body>
    <div class="content">
    <h2>This app will predict if a cardholder will default
    on their next payment.</h2>
    <a href="https://ccdr-265306.appspot.com/cardholder/data">
    <button class="button">Click to View Raw Data</button></a>
    <a href="https://development-dot-ccdr-265306.appspot.com/apidocs">
    <button class="button">Click to Make Predictions</button></a>
    </div>
    </body>
    </html>
    """


@app.route('/cardholder/data')
def raw_data():
    """Returns raw cardholder data as JSON response"""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket("ccdr-raw")
    blobs = bucket.list_blobs()
    data = pd.DataFrame()
    for blob in blobs:
        file = blob.download_as_string()
        data = data.append(pd.read_csv(BytesIO(file)))
    data.reset_index(drop=True, inplace=True)
    return jsonify(data.to_dict())


@app.route('/cardholder/attributes/api', methods=['GET'])
def list_attributes():
    """Return list of attributes and their data types


    GET /cardholder/attributes/api
    ---
    responses:
        200:
            description: Returns a list of attributes and their datatypes.

    """

    attributes = {'ID': 'Int', 'AGE': 'Int', 'SEX': 'String/Float',
                  'EDUCATION': 'String/Float', 'MARRIAGE': 'String/Float',
                  'LIMIT_BAL': 'Float', 'BILL_AMT1': 'Float',
                  'BILL_AMT2': 'Float', 'BILL_AMT3': 'Float',
                  'BILL_AMT4': 'Float', 'BILL_AMT5': 'Float',
                  'BILL_AMT6': 'Float', 'PAY_AMT1': 'Float',
                  'PAY_AMT2': 'Float', 'PAY_AMT3': 'Float',
                  'PAY_AMT4': 'Float', 'PAY_AMT5': 'Float',
                  'PAY_AMT6': 'Float', 'PAY_0': 'String/Float',
                  'PAY_2': 'String/Float', 'PAY_3': 'String/Float',
                  'PAY_4': 'String/Float', 'PAY_5': 'String/Float',
                  'PAY_6': 'String/Float'}

    return jsonify({'attributes': attributes})


@app.route('/cardholder/predictions/api', methods=['GET'])
def get_predictions():
    """ Make credit card default predictions on cardholder data

    ---
        consumes: application/json
        parameters:
            -   in: query
                name: fields
                type: string
                description: Fields to specify for results (default all)
                required: False
            -   in: query
                name: where
                type: string
                description: WHERE clause (default none)
                required: False
            -   in: query
                name: and_op
                type: string
                description: AND operator (default none)

        responses:
            200:
                description: Returns prediction results.

    """
    fields = request.args.get('fields')
    where = request.args.get('where')
    and_op = request.args.get('and_op')

    try:
        response = jsonify(predictions.predict_to_dict(fields, where, and_op))
    except:
        response = jsonify({'fields': fields, 'where': where,
                            'and_op': and_op, 'status': 'error'})

    return response


if __name__ == '__main__':
    app.run()
