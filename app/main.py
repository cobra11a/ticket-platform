

import os
import uuid
import boto3

from fastapi import FastAPI, HTTPException
from mangum import Mangum
from pydantic import BaseModel




app = FastAPI()


TABLE_NAME = os.getenv("TABLE_NAME", "tickets")

def get_table():
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(TABLE_NAME)

    return table



class TicketIn(BaseModel):
    title: str
    priority: str = "medium"



@app.post("/tickets", status_code=201)
def create_ticket(data: TicketIn):

    
    ticket = {
        "id": str(uuid.uuid4()),
        "title": data.title,
        "priority": data.priority,
        "status": "open"
    }

    table = get_table()
    table.put_item(Item=ticket)

    return ticket



@app.get("/tickets")
def list_tickets():

    
    table = get_table()

   
    response = table.scan()

   
    return response.get("Items", [])


@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: str):

    
    table = get_table()

    
    response = table.get_item(
        Key={"id": ticket_id}
    )

    
    item = response.get("Item")

    
    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    
    return item

handler = Mangum(app)
