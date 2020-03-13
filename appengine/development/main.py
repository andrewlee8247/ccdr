from flask import Flask, jsonify, request
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
    <h2>This app predicts if a credit cardholder will default
    on their next payment.</h2>
    <a href="https://development-dot-ccdr-265306.appspot.com/apidocs">
    <button class="button">Click to Make Predictions</button></a>
    </div>
    </body>
    </html>
    """


@app.route('/cardholder/attributes/api', methods=['GET'])
def list_attributes():
    """Return list of attributes and their data types


    GET /cardholder/attributes/api
    ---
    responses:
        200:
            description: Returns a list of attributes and their datatypes.

    """

    attributes = {'ID': 'String', 'AGE': 'Integer', 'SEX': 'Integer',
                  'EDUCATION': 'Integer', 'MARRIAGE': 'Integer',
                  'LIMIT_BAL': 'Float', 'BILL_AMT1': 'Float',
                  'BILL_AMT2': 'Float', 'BILL_AMT3': 'Float',
                  'BILL_AMT4': 'Float', 'BILL_AMT5': 'Float',
                  'BILL_AMT6': 'Float', 'PAY_AMT1': 'Float',
                  'PAY_AMT2': 'Float', 'PAY_AMT3': 'Float',
                  'PAY_AMT4': 'Float', 'PAY_AMT5': 'Float',
                  'PAY_AMT6': 'Float', 'PAY_0': 'Integer', 'PAY_2': 'Integer',
                  'PAY_3': 'Integer', 'PAY_4': 'Integer', 'PAY_5': 'Integer',
                  'PAY_6': 'Integer'}

    return jsonify({'attributes': attributes})


@app.route('/cardholder/predictions/api', methods=['GET'])
def get_predictions():
    """ Make credit card default predictions on cardholder data
    Documentation:

    Prediction data is based on a research case on customer defaults on credit card payments in Taiwan from
    April 2005 to September 2005. Through this API, predictions made can be used to help issuers determine
    who to give a credit card to and what limit to provide.

    Predictions are based on information from 24 variables. Details are outlined below.
    To get predictions, use the get attributes API to see what inputs are needed to get the results.
    All currency has been converted to US dollars.

    Names and Descriptions:

    ID: ID of each client
    LIMIT_BAL: Amount of given credit in US dollars (includes individual and family/supplementary credit)
    SEX: Gender (1=male, 2=female)
    EDUCATION: (1=graduate school, 2=university, 3=high school, 4=others)
    MARRIAGE: Marital status (1=married, 2=single, 3=others)
    AGE: Age in years
    PAY_0: Repayment status in September 2005 (-2=no consumption, -1=pay duly, 0=the use of revolving credit, 
    1=payment delay for one month, 2=payment delay for two months, … 8=payment delay for eight months, 
    9=payment delay for nine months and above)
    PAY_2: Repayment status in August 2005 (scale same as above)
    PAY_3: Repayment status in July 2005 (scale same as above)
    PAY_4: Repayment status in June 2005 (scale same as above)
    PAY_5: Repayment status in May 2005 (scale same as above)
    PAY_6: Repayment status in April 2005 (scale same as above)
    BILL_AMT1: Amount of bill statement in September 2005 (US dollar)
    BILL_AMT2: Amount of bill statement in August 2005 (US dollar)
    BILL_AMT3: Amount of bill statement in July 2005 (US dollar)
    BILL_AMT4: Amount of bill statement in June 2005 (US dollar)
    BILL_AMT5: Amount of bill statement in May 2005 (US dollar)
    BILL_AMT6: Amount of bill statement in April 2005 (US dollar)
    PAY_AMT1: Amount of previous payment in September 2005 (US dollar)
    PAY_AMT2: Amount of previous payment in August 2005 (US dollar)
    PAY_AMT3: Amount of previous payment in July 2005 (US dollar)
    PAY_AMT4: Amount of previous payment in June 2005 (US dollar)
    PAY_AMT5: Amount of previous payment in May 2005 (US dollar)
    PAY_AMT6: Amount of previous payment in April 2005 (US dollar)
    default_payment_next_month: Default payment (1=yes, 0=no)

    To get detailed documentation on classifications and the study visit:

    http://inseaddataanalytics.github.io/INSEADAnalytics/CourseSessions/ClassificationProcessCreditCardDefault.html

    Example Prediction:

    fields (case-insensitive): ID, AGE, LIMIT_BAL
    where (case-insensitive): AGE = 30
    and_op (case-insensitive): LIMIT_BAL > 1000
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
