from fastapi import FastAPI, HTTPException
import sqlite3

app = FastAPI()

def get_db_connection():
    conn = sqlite3.connect("data.db")  # Đổi tên file database tùy theo bạn
    return conn

def close_db_connection(conn):
    conn.close()

@app.get("/get_data")
def get_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM order_management"
    cursor.execute(query)

    rows = cursor.fetchall()

    data = [{'ID': row[0], 'Product_Name': row[1], 'Date': row[2], 'Must_Have': row[3], 'Nice_To_Have': row[4], 'Wasted': row[5]} for row in rows]

    cursor.close()
    close_db_connection(conn)

    return data

@app.delete("/delete_data/{data_id}")
def delete_data(data_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "DELETE FROM order_management WHERE id = ?"
    cursor.execute(query, (data_id,))

    conn.commit()
    cursor.close()
    close_db_connection(conn)

    return data_id

@app.post("/add_data")
def add_data(data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = "INSERT INTO order_management (product_name, date, must_have, nice_to_have, wasted) VALUES (?, ?, ?, ?, ?)"
        values = (data['product_name'], data['date'], data['must_have'], data['nice_to_have'], data['wasted'])
        cursor.execute(query, values)

        conn.commit()
        cursor.close()
        close_db_connection(conn)

        return {"message": "Data added successfully"}
    except sqlite3.Error as err:
        print("Database Error:", err)
        raise HTTPException(status_code=500, detail="Error adding data to the database")

@app.post("/create_table")
def create_table(table_info: dict):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        table_name = table_info["table_name"]
        columns = table_info["columns"]

        column_definitions = ", ".join([f"{col['name']} {col['type']}" for col in columns])
        query = f"CREATE TABLE {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, {column_definitions})"
        cursor.execute(query)

        # Add COLLATE for specific columns
        for col in columns:
            if col['name'] == 'product_name' or col['name'] == 'date':
                alter_query = f"ALTER TABLE {table_name} ALTER COLUMN {col['name']} SET DATA TYPE {col['type']} COLLATE utf8mb4_unicode_ci"
                cursor.execute(alter_query)

        # Commit the table creation
        conn.commit()

        # Transfer data from order_management to the new table
        transfer_query = f"INSERT INTO {table_name} SELECT * FROM order_management"
        cursor.execute(transfer_query)

        # Commit the data transfer
        conn.commit()

        # Clear data from order_management
        clear_query = "DELETE FROM order_management"
        cursor.execute(clear_query)

        # Commit the deletion
        conn.commit()

        cursor.close()
        close_db_connection(conn)

        return {"message": f"Table '{table_name}' created, data transferred, and old data cleared successfully"}
    except sqlite3.Error as err:
        cursor.close()
        close_db_connection(conn)
        print("Error creating table:", err)
        raise HTTPException(status_code=500, detail=f"Error creating table: {err}")







@app.get("/get_tables")
def get_tables():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SHOW TABLES")
        all_table_names = [table[0] for table in cursor.fetchall()]
        
        # Filter out the "order_management" table
        table_names = [table_name for table_name in all_table_names if table_name != "order_management"]

        cursor.close()
        conn.close()

        return {"tables": table_names}
    except sqlite3.Error as err:
        print("Database Error:", err)
        raise HTTPException(status_code=500, detail="Error fetching tables from the database")

@app.delete("/delete_table/{table_name}")
def delete_table(table_name: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = f"DROP TABLE IF EXISTS {table_name}"
        cursor.execute(query)

        conn.commit()
        cursor.close()
        close_db_connection(conn)

        return {"message": f"Table '{table_name}' deleted successfully"}
    except sqlite3.Error as err:
        print("Error deleting table:", err)
        cursor.close()
        close_db_connection(conn)
        raise HTTPException(status_code=500, detail=f"Error deleting table: {err}")

@app.get("/get_table_data/{table_name}")
def get_table_data(table_name: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)

        rows = cursor.fetchall()

        data = [{'ID': row[0], 'Product_Name': row[1], 'Date': row[2], 'Must_Have': row[3], 'Nice_To_Have': row[4], 'Wasted': row[5]} for row in rows]

        cursor.close()
        close_db_connection(conn)

        return data
    except sqlite3.Error as err:
        cursor.close()
        close_db_connection(conn)
        print("Database Error:", err)
        raise HTTPException(status_code=500, detail=f"Error fetching data from table '{table_name}': {err}")

@app.get("/check_api")
def check_connection():
    try:
        conn = get_db_connection()
        close_db_connection(conn)
        return {"message": "Connected to the database"}
    except sqlite3.Error as err:
        return {"message": "Failed to connect to the database"}
    
@app.get("/get_all_tables_and_data")
def get_all_tables_and_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SHOW TABLES")
        all_table_names = [table[0] for table in cursor.fetchall()]

        all_data = {}

        for table_name in all_table_names:
            if table_name != "order_management":
                query = f"SELECT * FROM {table_name}"
                cursor.execute(query)

                rows = cursor.fetchall()

                data = [{'ID': row[0], 'Product_Name': row[1], 'Date': row[2], 'Must_Have': row[3], 'Nice_To_Have': row[4], 'Wasted': row[5]} for row in rows]
                all_data[table_name] = data

        cursor.close()
        close_db_connection(conn)

        return all_data
    except sqlite3.Error as err:
        cursor.close()
        close_db_connection(conn)
        print("Database Error:", err)
        raise HTTPException(status_code=500, detail="Error fetching all tables and data from the database")


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port="8000")


