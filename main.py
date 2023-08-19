from fastapi import FastAPI, HTTPException
import mysql.connector

app = FastAPI()

def get_db_connection():
    db_config = {
        'host': '103.97.126.24',
        'user': 'beohbrrl_python_api',
        'password': 'nguyen2004nam',
        'database': 'beohbrrl_python_api',
        'charset': 'utf8mb4'
    }

    conn = mysql.connector.connect(**db_config)
    return conn

def close_db_connection(conn):
    conn.close()

@app.get("/get_data")
def get_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    query = 'SELECT * FROM timekeeping'
    cursor.execute(query)

    rows = cursor.fetchall()

    data = [{'ID': row[0], 'Name': row[1], 'Position': row[2], 'Date': row[3]} for row in rows]

    cursor.close()
    close_db_connection(conn)

    return data

@app.delete("/delete_data/{data_id}")
def delete_data(data_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "DELETE FROM timekeeping WHERE id = %s"
    cursor.execute(query, (data_id,))

    conn.commit()
    cursor.close()
    close_db_connection(conn)

    return {"message": f"Data with ID {data_id} has been deleted"}

@app.post("/add_data")
def add_data(data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = "INSERT INTO timekeeping (Name, Position, Date) VALUES (%s, %s, %s)"
        values = (data['Name'], data['Position'], data['Date'])
        cursor.execute(query, values)

        conn.commit()
        cursor.close()
        close_db_connection(conn)

        return {"message": "Data added successfully"}
    except mysql.connector.Error as err:
        print("Database Error:", err)
        raise HTTPException(status_code=500, detail="Error adding data to the database")
    
@app.put("/update_data/{data_id}")
def update_data(data_id: int, updated_data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = "UPDATE Timekeeping SET Name = %s, Position = %s, Date = %s WHERE ID = %s"
        values = (updated_data['Name'], updated_data['Position'], updated_data['Date'], data_id)
        cursor.execute(query, values)

        conn.commit()
        cursor.close()
        close_db_connection(conn)

        return {"message": f"Data with ID {data_id} updated successfully"}
    except mysql.connector.Error as err:
        cursor.close()
        close_db_connection(conn)
        raise HTTPException(status_code=500, detail="Error updating data in the database")



if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
