import os

os.environ["AWS_DEFAULT_REGION"] = "ap-south-1"
os.environ["AWS_ACCESS_KEY_ID"] = "testing"        # fake keys, only for tests
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"

import boto3
from fastapi.testclient import TestClient
from moto import mock_aws

from app.main import app, TABLE_NAME

client = TestClient(app)


def make_table():
    boto3.client("dynamodb").create_table(
        TableName=TABLE_NAME,
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )


@mock_aws
def test_create_and_get_ticket():
    make_table()
    created = client.post("/tickets", json={"title": "Test", "priority": "high"})
    assert created.status_code == 201

    ticket_id = created.json()["id"]
    fetched = client.get(f"/tickets/{ticket_id}")
    assert fetched.status_code == 200
    assert fetched.json()["title"] == "Test"

@mock_aws
def test_get_missing_ticket_returns_404():
    make_table()
    response = client.get("/tickets/does-not-exist")
    assert response.status_code == 404


@mock_aws
def test_list_tickets():
    make_table()
    client.post("/tickets", json={"title": "First", "priority": "low"})
    client.post("/tickets", json={"title": "Second", "priority": "high"})
    response = client.get("/tickets")
    assert response.status_code == 200
    assert len(response.json()) == 2


@mock_aws
def test_update_ticket():
    make_table()
    created = client.post("/tickets", json={"title": "Fix printer", "priority": "low"})
    ticket_id = created.json()["id"]

    response = client.put(f"/tickets/{ticket_id}", json={"status": "closed"})
    assert response.status_code == 200
    assert response.json()["status"] == "closed"
    assert response.json()["title"] == "Fix printer"
