from datetime import datetime
from sql_connection import get_sql_connection

def insert_order(connection, order):
    cursor = connection.cursor()

    # Insert into orders table (Make sure the column names match your database schema)
    order_query = "INSERT INTO grocery_store.order (customer_name, total_price, date_time) VALUES (%s, %s, %s)"
    order_data = (order['customer_name'], float(order['total_price']), datetime.now())  # Ensure grand_total is float
    cursor.execute(order_query, order_data)

    # Get the last inserted order_id
    order_id = cursor.lastrowid

    # Insert into order_details table (Fix column name and ensure correct placeholders)
    order_details_query = "INSERT INTO order_details (order_id, product_id, quntity, total_price) VALUES (%s, %s, %s, %s)"
    order_details_data = [
        (order_id, int(detail['product_id']), float(detail['quntity']), float(detail['total_price']))
        for detail in order['order_details']
    ]

    # Execute batch insert
    cursor.executemany(order_details_query, order_details_data)

    # Commit the transaction
    connection.commit()
    cursor.close()
    
    return order_id

if __name__ == '__main__':
    connection = get_sql_connection()
    print(insert_order(connection, {
        'customer_name': 'Fury',
        'grand_total': 350,  # Ensure it's a number
        'order_details': [
            {'product_id': 2, 'quantity': 2, 'total_price': 50},
            {'product_id': 3, 'quantity': 1, 'total_price': 30}
        ]
    }))
