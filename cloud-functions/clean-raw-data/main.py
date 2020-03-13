from google.cloud import storage
from google.cloud.storage import Blob
import pandas as pd
import pyarrow
from io import BytesIO
import uuid
import os
import random
import warnings

warnings.filterwarnings("ignore")


def data_prep(event, context):
    # Impute null, merge categorical values, 
    # transform and convert to parquet, upload to cloud storage
    storage_client = storage.Client()
    bucket = storage_client.get_bucket("ccdr-raw")
    target = storage_client.get_bucket("ccdr-cleaned")
    blobs = bucket.list_blobs()
    data = pd.DataFrame()
    for blob in blobs:
        file = blob.download_as_string()
        data = data.append(pd.read_csv(BytesIO(file)))
    data.drop(['placeholder'], inplace=True, axis=1)
    data = data.rename(columns=data.iloc[0]).drop(data.index[0])
    data = data.rename(columns={'default payment next month': 'default_payment_next_month'})
    data = data[['ID', 'LIMIT_BAL', 'SEX', 'EDUCATION', 'MARRIAGE', 'AGE', 'PAY_0', 'PAY_2', 'PAY_3',
                'PAY_4', 'PAY_5', 'PAY_6', 'BILL_AMT1', 'BILL_AMT2', 'BILL_AMT3', 'BILL_AMT4',
                'BILL_AMT5', 'BILL_AMT6', 'PAY_AMT1', 'PAY_AMT2', 'PAY_AMT3', 'PAY_AMT4',
                'PAY_AMT5', 'PAY_AMT6', 'default_payment_next_month']]
    data['SEX'].fillna(data['SEX'].mode()[0], inplace=True)
    data['SEX'].replace('', data['SEX'].mode()[0], inplace=True)
    data['EDUCATION'].fillna(4, inplace=True)
    data['EDUCATION'].replace('', 4, inplace=True)
    data['EDUCATION'].replace(0, 4, inplace=True)
    data['EDUCATION'].replace(5, 4, inplace=True)
    data['EDUCATION'].replace(6, 4, inplace=True)
    data['MARRIAGE'].fillna(3, inplace=True)
    data['MARRIAGE'].replace('', 3, inplace=True)
    data['MARRIAGE'].replace(0, 3, inplace=True)
    data['AGE'].fillna(data['AGE'].median(), inplace=True)
    data['AGE'].replace('', data['AGE'].median(), inplace=True)
    data['AGE'].replace(0, data['AGE'].median(), inplace=True)
    data.iloc[:, 6:11].fillna(data.mode().iloc[0], inplace=True)
    data.iloc[:, 6:11].replace('', data.mode().iloc[0], inplace=True)
    data['default_payment_next_month'].fillna(data['default_payment_next_month'].mode()[0], inplace=True)
    data['default_payment_next_month'].replace('', data['default_payment_next_month'].mode()[0], inplace=True)
    data = data.apply(lambda x: x.fillna(x.median()), axis=0)
    data = data.apply(lambda x: x.replace('', x.median()), axis=0)
    data['default_payment_next_month'] =  data['default_payment_next_month'].astype('float32')
    data['default_payment_next_month'] =  data['default_payment_next_month'].astype('int16')
    data.iloc[:, 2:12] = data.iloc[:, 2:12].astype('float32')
    data.iloc[:, 2:12] = data.iloc[:, 2:12].astype('int16')
    data['LIMIT_BAL'] = round(data['LIMIT_BAL'].astype('float') * 0.033, 2)
    data.iloc[:, 12:24] = round(data.iloc[:, 12:24].astype('float') * 0.033, 2)
    data['ID'] = data['ID'].astype('float')
    data['ID'] = data['ID'].astype('int')
    rd = random.Random()
    rd.seed(40)
    data['ID'] = data['ID'].apply(lambda x: str(uuid.UUID(int=rd.getrandbits(128))))
    data.to_parquet('/tmp/cleaned.parquet', index=False)
    blob = Blob('cleaned.parquet', target)
    blob.upload_from_filename('/tmp/cleaned.parquet')
    os.remove('/tmp/cleaned.parquet')

    return
