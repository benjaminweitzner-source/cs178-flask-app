# dbCode.py
# Author: Bens
# Helper functions for database connection and queries

import pymysql
import creds

def get_conn():
    """Returns a connection to the MySQL RDS instance."""
    conn = pymysql.connect(
        host=creds.host,
        user=creds.user,
        password=creds.password,
        db=creds.db,
    )
    return conn

def execute_query(query, args=()):
    """Executes a SELECT query and returns all rows as dictionaries."""
    cur = get_conn().cursor(pymysql.cursors.DictCursor)
    cur.execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows

import boto3

REGION = "us-east-1"
TABLE_NAME = "Inbound_Inv"

def get_dynamo_table():
    """Return a reference to the DynamoDB InboundOrders table."""
    dynamodb = boto3.resource("dynamodb", region_name=REGION)
    return dynamodb.Table(TABLE_NAME)

def get_all_orders():
    """Scan the entire InboundOrders table and return all items."""
    table = get_dynamo_table()
    response = table.scan()
    return response.get("Items", [])

def add_order(order_id, item_description, quantity, supplier):
    """Put a new order into the InboundOrders table."""
    table = get_dynamo_table()
    table.put_item(Item={
        "order_id": order_id,
        "item_description": item_description,
        "quantity": quantity,
        "supplier": supplier
    })

def delete_order(order_id):
    """Delete an order from the InboundOrders table by order_id."""
    table = get_dynamo_table()
    table.delete_item(Key={"order_id": order_id})

def update_order(order_id, quantity):
    """Update the quantity of an order in DynamoDB."""
    table = get_dynamo_table()
    table.update_item(
        Key={"order_id": order_id},
        UpdateExpression="SET quantity = :q",
        ExpressionAttributeValues={":q": quantity}
    )