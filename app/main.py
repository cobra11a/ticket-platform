

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

class TicketUpdate(BaseModel):
    title: str | None = None
    priority: str | None = None
    status: str | None = None



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

@app.put("/tickets/{ticket_id}")
def update_ticket(ticket_id: str, data: TicketUpdate):
    table = get_table()
    item = table.get_item(Key={"id": ticket_id}).get("Item")
    if item is None:
        raise HTTPException(
                    status_code=404,
                    detail="Ticket not found"
                )
    changes = data.model_dump(exclude_unset=True)
    item.update(changes)
    table.put_item(Item=item)
    return item

@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id:str):
    table = get_table()

    item = table.get_item(Key={"id":ticket_id}).get("Item")
    if item is None:
        raise HTTPException(status_code=404,detail="Ticket not found")
    table.delete_item(Key={"id":ticket_id})
    return{"message": "Ticket deleted"}

handler = Mangum(app)
