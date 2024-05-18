from fastapi import FastAPI, HTTPException
import mysql.connector
import schemas
import db

app = FastAPI()

@app.get("/clients")
def get_clients():
    mysql_db = mysql.connector.connect(host=db.host_name, port=db.port_number, user=db.user_name, password=db.password_db, database=db.database_name)
    cursor = mysql_db.cursor()
    cursor.execute("SELECT * FROM clients")
    result = cursor.fetchall()
    mysql_db.close()
    cursor.close()
    return {"clients": result}

@app.get("/client/{id}")
def get_client_by_id(id: int):
    mysql_db = mysql.connector.connect(host=db.host_name, port=db.port_number, user=db.user_name, password=db.password_db, database=db.database_name)
    cursor = mysql_db.cursor()
    cursor.execute(f"SELECT * FROM clients WHERE id = {id}")
    result = cursor.fetchone()
    mysql_db.close()
    cursor.close()

    if result:
        return {"client": result}
    else:
        raise HTTPException(status_code=404, detail="Client not found")

@app.post("/clients")
def create_client(client: schemas.Client):
    mysql_db = mysql.connector.connect(host=db.host_name, port=db.port_number, user=db.user_name, password=db.password_db, database=db.database_name)
    cursor = mysql_db.cursor()

    cursor.execute("SELECT id FROM clients WHERE id = %s", (client.id,))
    existing_client = cursor.fetchone()
    if existing_client:
        mysql_db.close()
        cursor.close()
        raise HTTPException(status_code=400, detail="ID already exist")

    id = client.id
    name = client.name
    email = client.email
    phone = client.phone
    address = client.address
    registration_date = client.registration_date

    sql = "INSERT INTO clients (id, name, email, phone, address, registration_date) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (id, name, email, phone, address, registration_date)
    cursor.execute(sql, val)
    mysql_db.commit()
    mysql_db.close()
    cursor.close()
    return {"message": "Client added successfully"}

@app.put("/clients/{id}")
def update_client(id: int, client: schemas.Client):
    mysql_db = mysql.connector.connect(host=db.host_name, port=db.port_number, user=db.user_name, password=db.password_db, database=db.database_name)
    cursor = mysql_db.cursor()

    name = client.name
    email = client.email
    phone = client.phone
    address = client.address
    registration_date = client.registration_date

    sql = "UPDATE clients SET name=%s, email=%s, phone=%s, address=%s, registration_date=%s WHERE id=%s"
    val = (name, email, phone, address, registration_date, id)
    cursor.execute(sql, val)
    mysql_db.commit()
    mysql_db.close()
    cursor.close()
    return {"message": "Client updated successfully"}

@app.delete("/clients/{id}")
def delete_client(id: int):
    mysql_db = mysql.connector.connect(host=db.host_name, port=db.port_number, user=db.user_name, password=db.password_db, database=db.database_name)
    cursor = mysql_db.cursor()

    cursor.execute("SELECT id FROM clients WHERE id = %s", (id,))
    existing_client = cursor.fetchone()
    if not existing_client:
        mysql_db.close()
        cursor.close()
        raise HTTPException(status_code=404, detail="Client not found")

    cursor.execute(f"DELETE FROM clients WHERE id = {id}")
    mysql_db.commit()
    mysql_db.close()
    cursor.close()
    return {"message": "Client deleted successfully"}

