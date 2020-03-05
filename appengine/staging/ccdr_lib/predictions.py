from google.cloud import bigquery
import pandas as pd


def and_to_op(c):
    c = list(c.split(','))
    c_list = []
    for i in range(len(c)):
        c_list.append('AND'.ljust(4) + c[i].strip())

    c_list = ' '.join([str(elem) for elem in c_list])

    return c_list


def get_predict_query(fields=None, where=None, and_op=None):
    database = 'ccdr-265306'
    client = bigquery.Client(database)
    dataset = client.dataset('ccdr_database')
    table = dataset.table('credit_cardholder_data')
    if table is None:
        pass
    if fields is None:
        fields = '*'
    else:
        fields = 'predicted_default_payment_next_month,'.rjust(38) \
        + 'predicted_default_payment_next_month_probs,' \
        + str(fields).rjust(len(fields) + 1).upper()
    if where is None:
        where = ''
    else:
        where = '\n \t WHERE' + ' ' + str(where).ljust(len(where) + 1).upper()
    if and_op is None:
        and_op = ''
    else:
        and_op = and_to_op(and_op).upper()
    query = """
    SELECT""" + str(fields) + """
    FROM
      ML.PREDICT(MODEL `ccdr-265306.ccdr_database.class_model_5`,
        (
        SELECT
          CAST(ID AS INT64) AS ID,
          CAST(AGE AS INT64) AS AGE,
          CAST(SEX AS string) AS SEX,
          CAST(EDUCATION AS string) AS EDUCATION,
          CAST(MARRIAGE AS string) AS MARRIAGE,
          LIMIT_BAL,
          BILL_AMT1,
          BILL_AMT2,
          BILL_AMT3,
          BILL_AMT4,
          BILL_AMT5,
          BILL_AMT6,
          PAY_AMT1,
          PAY_AMT2,
          PAY_AMT3,
          PAY_AMT4,
          PAY_AMT5,
          PAY_AMT6,
          CAST(PAY_0 AS string) AS PAY_0,
          CAST(PAY_2 AS string) AS PAY_2,
          CAST(PAY_3 AS string) AS PAY_3,
          CAST(PAY_4 AS string) AS PAY_4,
          CAST(PAY_5 AS string) AS PAY_5,
          CAST(PAY_6 AS string) AS PAY_6
        FROM
          `ccdr_database.credit_cardholder_data`""" \
    + str(where) \
    + str(and_op) \
    + """
          ),
           STRUCT(0.2430 AS threshold)
        )
    """
    query_job = client.query(query)
    results = query_job.result()

    return results


def predict_to_dict(fields=None, where=None, and_op=None):
    results = get_predict_query(fields, where, and_op)

    predictions = []
    for row in results:
        predictions.append(row)

    clean_list = []
    for i in range(len(predictions)):
        init_list = list(predictions[i][2:])
        init_list.insert(0, predictions[i][0])
        init_list.insert(1, predictions[i][1][0]['prob'])
        init_list.insert(2, predictions[i][1][1]['prob'])
        clean_list.append(init_list)

    if fields is None:
        column_list = ['predicted_default_payment_next_month', 'prob_of_default', 'prob_of_no_default',
                       'ID', 'AGE', 'SEX', 'EDUCATION', 'MARRIAGE', 'LIMIT_BAL', 'BILL_AMT1', 'BILL_AMT2',
                       'BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6', 'PAY_AMT1', 'PAY_AMT2', 'PAY_AMT3',
                       'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6', 'PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6']
    else:
        column_list = fields.replace(' ', '').upper().split(',')
        column_list.insert(0, 'predicted_default_payment_next_month')
        column_list.insert(1, 'prob_of_default')
        column_list.insert(2, 'prob_of_no_default')

    df = pd.DataFrame(clean_list, columns=column_list)

    return df.to_dict('list')
