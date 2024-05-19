# main.py

from fastapi import FastAPI, HTTPException
import mysql.connector
from schemas import Policy

app = FastAPI()

# Configuración de la base de datos
host_name = "52.2.83.96"
port_number = "8005"
user_name = "root"
password_db = "utec"
database_name = "bd_api_pymes_insurance"

# Conectar a la base de datos
mydb = mysql.connector.connect(
    host=host_name,
    port=port_number,
    user=user_name,
    password=password_db,
    database=database_name
)

# Endpoint para obtener todas las pólizas de seguro
@app.get("/policies/")
def get_policies():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM policies")
    policies = cursor.fetchall()
    cursor.close()
    return {"policies": policies}

# Endpoint para obtener una póliza de seguro por ID
@app.get("/policies/{policy_id}")
def get_policy(policy_id: int):
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM policies WHERE id = %s", (policy_id,))
    policy = cursor.fetchone()
    cursor.close()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return policy

# Endpoint para crear una nueva póliza de seguro
@app.post("/policies/")
def create_policy(policy: Policy):
    cursor = mydb.cursor()
    cursor.execute("INSERT INTO policies (name, description, coverage, premium, deductible, coverage_limit, start_date, end_date, company, contact_person, contact_email, contact_phone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   (policy.name, policy.description, policy.coverage, policy.premium, policy.deductible, policy.coverage_limit, policy.start_date, policy.end_date, policy.company, policy.contact_person, policy.contact_email, policy.contact_phone))
    mydb.commit()
    cursor.close()
    return {"message": "Policy created successfully"}

# Endpoint para actualizar una póliza de seguro existente
@app.put("/policies/{policy_id}")
def update_policy(policy_id: int, policy: Policy):
    cursor = mydb.cursor()
    cursor.execute("UPDATE policies SET name = %s, description = %s, coverage = %s, premium = %s, deductible = %s, coverage_limit = %s, start_date = %s, end_date = %s, company = %s, contact_person = %s, contact_email = %s, contact_phone = %s WHERE id = %s",
                   (policy.name, policy.description, policy.coverage, policy.premium, policy.deductible, policy.coverage_limit, policy.start_date, policy.end_date, policy.company, policy.contact_person, policy.contact_email, policy.contact_phone, policy_id))
    mydb.commit()
    cursor.close()
    return {"message": "Policy updated successfully"}

# Endpoint para eliminar una póliza de seguro por ID
@app.delete("/policies/{policy_id}")
def delete_policy(policy_id: int):
    cursor = mydb.cursor()
    cursor.execute("DELETE FROM policies WHERE id = %s", (policy_id,))
    mydb.commit()
    cursor.close()
    return {"message": "Policy deleted successfully"}
