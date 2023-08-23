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
def create_table(data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        table_name = data['table_name']
        columns = data['columns']

        column_definitions = ', '.join([
            f"{column['name']} {column['type']}" for column in columns
        ])

        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions})"
        cursor.execute(query)

        conn.commit()
        cursor.close()
        close_db_connection(conn)

        return {"message": "Table created successfully"}
    except sqlite3.Error as err:
        print("Database Error:", err)
        raise HTTPException(status_code=500, detail="Error creating table")








@app.get("/get_tables")
def get_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        cursor.execute(query)

        tables = [table[0] for table in cursor.fetchall()]

        cursor.close()
        close_db_connection(conn)

        return {"tables": tables}
    except sqlite3.Error as err:
        print("Database Error:", err)
        raise HTTPException(status_code=500, detail="Error getting tables")


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


    



@app.post('/create_table_and_copy_data')
def create_table_and_copy_data(request: dict):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Tạo bảng mới
        new_table_name = request.get("new_table_name")
        new_table_columns = [
            {"name": "id", "type": "INTEGER PRIMARY KEY"},
            {"name": "product_name", "type": "TEXT"},
            {"name": "date", "type": "TEXT"},
            {"name": "must_have", "type": "INTEGER"},
            {"name": "nice_to_have", "type": "INTEGER"},
            {"name": "wasted", "type": "INTEGER"}
        ]
        column_definitions = ', '.join([
            f"{column['name']} {column['type']}" for column in new_table_columns
        ])
        create_table_query = f"CREATE TABLE IF NOT EXISTS {new_table_name} ({column_definitions})"
        cursor.execute(create_table_query)
        conn.commit()

        # Chuyển dữ liệu từ bảng cũ sang bảng mới
        transfer_data_query = f"INSERT INTO {new_table_name} SELECT * FROM order_management"
        cursor.execute(transfer_data_query)
        conn.commit()

        cursor.close()
        close_db_connection(conn)

        return {"message": "Table created and data transferred successfully"}
    except sqlite3.Error as err:
        print("Database Error:", err)
        raise HTTPException(status_code=500, detail="Error creating table and transferring data")


@app.delete('/delete_old_data')
def delete_old_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Xóa dữ liệu của bảng cũ
        delete_query = "DELETE FROM order_management"  # Thay thế old_table_name bằng tên thực tế của bảng cũ
        cursor.execute(delete_query)
        conn.commit()

        cursor.close()
        close_db_connection(conn)

        return {"message": "Old data deleted successfully"}
    except sqlite3.Error as err:
        print("Database Error:", err)
        raise HTTPException(status_code=500, detail="Error deleting old data")



if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port="8000")


