from fastapi import FastAPI, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import boto3
import os

my_session = boto3.session.Session(
    aws_access_key_id=os.environ.get("ACCESS_KEY"),
    aws_secret_access_key=os.environ.get("SECRET_KEY"),
    region_name = "us-east-1",
)

table_name = os.environ['TABLE_NAME']
table = my_session.resource('dynamodb').Table(table_name)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://jtschuwirth.xyz",
    "https://www.jtschuwirth.xyz"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/nuncanunca/online/chat")
def getPlayersInChat(
    response: Response,
    id: int=0
    ):
    try:
        connection_ids = []
        scan_response = table.scan()
        for item in scan_response['Items']:
            if item["turn_status"] == "hosting": 
                    continue
            connection_ids.append(item["connection_id"])
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    response.status_code=status.HTTP_200_OK
    return connection_ids


#uvicorn lambda_function:app --reload --port 8081
lambda_handler = Mangum(app, lifespan="off")