# main.py

from fastapi import FastAPI, HTTPException
from typing import List
import mysql.connector
import schemas

app = FastAPI()

host_name = "52.2.83.96"
port_number = "8010"
user_name = "root"
password_db = "utec"
database_name = "bd_api_insurance_pyme"  

# Obtener todas las pólizas
@app.get("/policies", response_model=List[schemas.Policy])
def get_policies():
    try:
        mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)  
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM policies")
        result = cursor.fetchall()
        mydb.close()
        policies = []
        for row in result:
            policies.append({"policy_number": row[0], "company_name": row[1], "coverage": row[2], "premium_amount": row[3], "expiration_date": row[4], "active": bool(row[5])})
        return policies
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

# Obtener una póliza por número de póliza
@app.get("/policies/{policy_number}", response_model=schemas.Policy)
def get_policy(policy_number: str):
    try:
        mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)  
        cursor = mydb.cursor()
        cursor.execute(f"SELECT * FROM policies WHERE policy_number = '{policy_number}'")
        result = cursor.fetchone()
        mydb.close()
        if result:
            return {"policy_number": result[0], "company_name": result[1], "coverage": result[2], "premium_amount": result[3], "expiration_date": result[4], "active": bool(result[5])}
        else:
            raise HTTPException(status_code=404, detail="Policy not found")
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

# Agregar una nueva póliza
@app.post("/policies", response_model=schemas.Policy)
def add_policy(policy: schemas.Policy):
    try:
        mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)  
        cursor = mydb.cursor()
        sql = "INSERT INTO policies (policy_number, company_name, coverage, premium_amount, expiration_date, active) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (policy.policy_number, policy.company_name, policy.coverage, policy.premium_amount, policy.expiration_date, policy.active)
        cursor.execute(sql, val)
        mydb.commit()
        mydb.close()
        return policy
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

# Modificar una póliza
@app.put("/policies/{policy_number}", response_model=schemas.Policy)
def update_policy(policy_number: str, policy: schemas.Policy):
    try:
        mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)  
        cursor = mydb.cursor()
        sql = "UPDATE policies SET company_name = %s, coverage = %s, premium_amount = %s, expiration_date = %s, active = %s WHERE policy_number = %s"
        val = (policy.company_name, policy.coverage, policy.premium_amount, policy.expiration_date, policy.active, policy_number)
        cursor.execute(sql, val)
        mydb.commit()
        mydb.close()
        return policy
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

# Eliminar una póliza
@app.delete("/policies/{policy_number}")
def delete_policy(policy_number: str):
    try:
        mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)  
        cursor = mydb.cursor()
        cursor.execute(f"DELETE FROM policies WHERE policy_number = '{policy_number}'")
        mydb.commit()
        mydb.close()
        return {"message": "Policy deleted successfully"}
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
