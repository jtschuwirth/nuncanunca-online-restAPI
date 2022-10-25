from fastapi import FastAPI, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from functions.initTable import initTable

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
def getPlayersInRoom(
    response: Response,
    id: str="aaaa"
    ):
    try:
        table = initTable()
        players = []
        scan_response = table.scan(
            FilterExpression="room_id = :id",
            ExpressionAttributeValues={
                ":id": id.upper() 
            })
        for item in scan_response['Items']:
            if item["turn_status"] == "hosting": 
                    continue
            players.append({
                "connection_id": item["connection_id"], 
                "user_name":item["user_name"],
                "points":item["points"]
                })
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    response.status_code=status.HTTP_200_OK
    return players

@app.post("/nuncanunca/online/changelevel")
def changeLevel(
    response: Response,
    room_id: str,
    level: int=1
    ):
    try:
        table = initTable()
        scan_response = table.scan(
            FilterExpression="room_id = :id",
            ExpressionAttributeValues={
                ":id": room_id   
        })
        
        for item in scan_response['Items']:
            if item["turn_status"] == "hosting":
                connection_id = item["connection_id"]

        table.update_item(
            Key={'connection_id': connection_id},
            UpdateExpression = "SET lvl = :lvl",
            ExpressionAttributeValues={
                ':lvl': level
        })

    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    response.status_code=status.HTTP_200_OK
    return "Success"

#uvicorn lambda_function:app --reload --port 8081
lambda_handler = Mangum(app, lifespan="off")