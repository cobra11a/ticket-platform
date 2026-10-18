# Serverless Ticket Management API

A RESTful helpdesk ticket API built with **Python, FastAPI and AWS DynamoDB**, designed to run serverless on **AWS Lambda** and provisioned with **Terraform**.

## What it does
Users report problems (for example "Outlook not opening"), and support teams can track each ticket from creation to closure.

## Architecture

~~~
Client -> API Gateway -> Lambda (FastAPI + Mangum) -> DynamoDB
~~~

## Tech stack
- **Python 3.12**, **FastAPI**, Pydantic
- **AWS DynamoDB** (boto3), **AWS Lambda** (Mangum adapter)
- **Terraform** for infrastructure as code
- **pytest** with **moto** (mocked DynamoDB, so tests need no AWS account)
- **Git / GitHub**, developed in GitHub Codespaces

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/tickets` | Create a ticket |
| GET | `/tickets` | List all tickets |
| GET | `/tickets/{ticket_id}` | Get one ticket |
| PUT | `/tickets/{ticket_id}` | Update title, priority or status |
| DELETE | `/tickets/{ticket_id}` | Delete a ticket |

Ticket ids are UUID strings, because DynamoDB has no auto-increment keys.

## Run the tests

~~~bash
pip install -r requirements.txt
python -m pytest -v
~~~

All 5 tests run against a mocked DynamoDB table.

## Project structure

~~~
app/main.py          FastAPI application and DynamoDB logic
tests/test_api.py    pytest tests (moto)
terraform/main.tf    Infrastructure as code (DynamoDB table so far)
requirements.txt     Python dependencies
~~~

## Status
- [x] CRUD endpoints with validation and 404 handling
- [x] Automated tests (5 passing)
- [x] Terraform: DynamoDB table
- [ ] Terraform: Lambda function and API Gateway
- [ ] Deployment to AWS

## What I learned
- Designing REST endpoints and handling errors such as a missing ticket
- Why NoSQL needs generated ids, and how DynamoDB's response shape differs from SQL
- Writing tests that catch real bugs, including one in my own update endpoint
