import boto3
import os
from dotenv import load_dotenv
load_dotenv()

def initTable():
    my_session = boto3.session.Session(
        aws_access_key_id=os.environ.get("ACCESS_KEY"),
        aws_secret_access_key=os.environ.get("SECRET_KEY"),
        region_name = "us-east-1",
    )
    table_name = os.environ['TABLE_NAME']
    table = my_session.resource('dynamodb').Table(table_name)
    return table