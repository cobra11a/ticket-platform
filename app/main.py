from fastapi import FastAPI , HTTPException

app = FastAPI()

tickets = []

@app.post("/tickets")
def create_ticket(title: str, priority: str = "medium"):

    ticket = {
        "id": len(tickets) + 1,
        "title": title,
        "priority": priority,
        "status": "open"
        }
    tickets.append(ticket)
    return ticket

@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int):

     for ticket in tickets:
        if ticket["id"] == ticket_id:
                return ticket

     raise HTTPException(status_code=404,detail="Ticket not found")

@app.put("/tickets/{ticket_title}")
def put_ticket(ticket_title,new_title):

     for ticket in tickets:
          if ticket["title"] ==ticket_title:
               ticket["title"] = new_title
               return ticket
     raise HTTPException(status_code=404,detail="Ticket not found")