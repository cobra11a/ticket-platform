# Serverless Ticket Management API

A RESTful helpdesk ticket API built with **Python, FastAPI and AWS DynamoDB**, running serverless on **AWS Lambda** and provisioned with **Terraform**.

## What it does
Users report problems (for example "Outlook not opening"), and support teams can track each ticket from creation to closure.

## Architecture

~~~
Client -> API Gateway (HTTP API) -> Lambda (FastAPI + Mangum) -> DynamoDB
~~~

- **API Gateway**: public HTTPS endpoint that forwards every request to Lambda
- **Lambda**: runs the FastAPI app through Mangum (Python 3.12)
- **DynamoDB**: `tickets` table in on-demand mode, partition key `id`
- **IAM**: Lambda role limited to the `tickets` table plus CloudWatch logs
- **Region**: ap-south-1 (Mumbai)

## Tech stack
- **Python 3.12**, **FastAPI**, Pydantic
- **AWS DynamoDB** (boto3), **AWS Lambda** (Mangum adapter), **API Gateway**
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

## Deploy to AWS

Prerequisites: AWS CLI configured (`aws sts get-caller-identity` works) and Terraform installed.

1. Build the Lambda package:

~~~bash
rm -rf build && mkdir -p build/pkg
pip install -r requirements-lambda.txt -t build/pkg \
  --platform manylinux2014_x86_64 --only-binary=:all: --python-version 3.12
cp app/main.py build/pkg/
cd build/pkg && zip -r ../lambda.zip . -x "*.pyc" "*__pycache__*" && cd ../..
~~~

2. Create the infrastructure:

~~~bash
cd terraform
terraform init
terraform plan
terraform apply
~~~

3. Try the API with the URL printed as `api_url`:

~~~bash
curl -X POST "<api_url>/tickets" \
  -H "Content-Type: application/json" \
  -d '{"title":"First ticket"}'
curl "<api_url>/tickets"
~~~

## Cleanup

Remove all AWS resources when you are done:

~~~bash
cd terraform
terraform destroy
~~~

## Project structure

~~~
app/main.py                  FastAPI application and DynamoDB logic
tests/test_api.py            pytest tests (moto)
terraform/providers.tf       AWS provider and region
terraform/variables.tf       Input variables
terraform/dynamodb.tf        DynamoDB table
terraform/iam.tf             Lambda execution role and permissions
terraform/lambda.tf          Lambda function
terraform/api_gateway.tf     HTTP API in front of Lambda
terraform/outputs.tf         API URL, table name, function name
requirements.txt             Dependencies for local development and tests
requirements-lambda.txt      Runtime dependencies packaged into the Lambda zip
~~~

## Status
- [x] CRUD endpoints with validation and 404 handling
- [x] Automated tests (5 passing)
- [x] Terraform: DynamoDB table
- [x] Terraform: IAM role for Lambda
- [x] Terraform: Lambda function and API Gateway
- [x] Deployed to AWS (ap-south-1) and all endpoints verified with curl
- [ ] Architecture diagram
- [ ] Authentication on the API

## What I learned
- Designing REST endpoints and handling errors such as a missing ticket
- Why NoSQL needs generated ids, and how DynamoDB's response shape differs from SQL
- Writing tests that catch real bugs, including one in my own update endpoint
- Debugging real mistakes: DynamoDB's `Item` key is case-sensitive, and an endpoint that