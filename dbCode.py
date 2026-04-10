# dbCode.py
# Author: Ben
# Helper functions for database connection and queries

import pymysql
import boto3
import creds

REGION = "us-east-1"
TABLE_NAME = "Inbound_Inv"

def get_conn():
    """Returns a connection to the MySQL RDS instance."""
    conn = pymysql.connect(
        host=creds.host,
        user=creds.user,
        password=creds.password,
        db=creds.db,
    )
    return conn

def get_dynamo_table():
    """Return a reference to the DynamoDB Inbound_Inv table."""
    dynamodb = boto3.resource("dynamodb", region_name=REGION)
    return dynamodb.Table(TABLE_NAME)

def execute_query(query, args=()):
    """Executes a SELECT query and returns all rows as dictionaries."""
    try:
        cur = get_conn().cursor(pymysql.cursors.DictCursor)
        cur.execute(query, args)
        rows = cur.fetchall()
        cur.close()
        return rows
    except Exception as e:
        print("Database error:", e)
        return []

def add_inventory_item(description, price, category_id):
    """Insert a new item into the Inventory table."""
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("INSERT INTO Inventory (description, price, categoryID) VALUES (%s, %s, %s)",
                   (description, price, category_id))
        conn.commit()
        cur.close()
    except Exception as e:
        print("Database error:", e)

def delete_inventory_item(item_id):
    """Delete an item from the Inventory table by ID."""
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM Inventory WHERE ID = %s", (item_id,))
        conn.commit()
        cur.close()
    except Exception as e:
        print("Database error:", e)

def get_all_orders():
    """Scan the entire Inbound_Inv table and return all items."""
    try:
        table = get_dynamo_table()
        response = table.scan()
        return response.get("Items", [])
    except Exception as e:
        print("DynamoDB error:", e)
        return []

def add_order(order_id, item_description, quantity, supplier):
    """Put a new order into the Inbound_Inv table."""
    try:
        table = get_dynamo_table()
        table.put_item(Item={
            "order_id": order_id,
            "item_description": item_description,
            "quantity": quantity,
            "supplier": supplier
        })
    except Exception as e:
        print("DynamoDB error:", e)

def delete_order(order_id):
    """Delete an order from the Inbound_Inv table by order_id."""
    try:
        table = get_dynamo_table()
        table.delete_item(Key={"order_id": order_id})
    except Exception as e:
        print("DynamoDB error:", e)

def update_order(order_id, quantity):
    """Update the quantity of an order in DynamoDB."""
    try:
        table = get_dynamo_table()
        table.update_item(
            Key={"order_id": order_id},
            UpdateExpression="SET quantity = :q",
            ExpressionAttributeValues={":q": quantity}
        )
    except Exception as e:
        print("DynamoDB error:", e)