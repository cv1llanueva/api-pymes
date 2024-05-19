from fastapi import FastAPI, HTTPException, status
import mysql.connector
import schemas
from typing import List
import uuid

app = FastAPI()

host_name = "52.2.83.96"
port_number = "8005"
user_name = "root"
password_db = "utec"
database_name = "bd_api_pymes" 

def connect_to_db():
    return mysql.connector.connect(
        host=host_name,
        port=port_number,
        user=user_name,
        password=password_db,
        database=database_name
    )

# Obtener todos los seguros asociados a las Pymes
@app.get("/pymes", response_model=List[schemas.PymeOutput])
def get_pymes():
    mydb = connect_to_db()
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.pymesId, p.total_employee, p.average_age, p.is_private, p.bedded, p.is_sorted_ascending, p.register_date,
               pr.productId, pr.coverageId, pr.product_name, pr.product_options, pr.top_feature, pr.inpatient,
               pr.outpatient_gp, pr.outpatient_sp, pr.outpatient_dental, pr.personal_accident, pr.term_life, pr.critical_illness,
               pr.premium_per_pax, pr.total_premium
        FROM Pymes p
        LEFT JOIN Products pr ON p.pymesId = pr.pymesId
    """)
    result = cursor.fetchall()
    mydb.close()
    if not result:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No Pyme's products found")
    pymes = {}
    for row in result:
        pyme_id = row['pymesId']
        if pyme_id not in pymes:
            pymes[pyme_id] = {
                "pymesId": row["pymesId"],
                "total_employee": row["total_employee"],
                "average_age": row["average_age"],
                "is_private": row["is_private"],
                "bedded": row["bedded"],
                "is_sorted_ascending": row["is_sorted_ascending"],
                "register_date": row["register_date"],
                "products": []
            }
        if row["productId"]:
            pymes[pyme_id]["products"].append({
                "productId": row["productId"],
                "pymesId": row["pymesId"],
                "coverageId": row["coverageId"],
                "product_name": row["product_name"],
                "product_options": row["product_options"],
                "top_feature": row["top_feature"],
                "inpatient": row["inpatient"],
                "outpatient_gp": row["outpatient_gp"],
                "outpatient_sp": row["outpatient_sp"],
                "outpatient_dental": row["outpatient_dental"],
                "personal_accident": row["personal_accident"],
                "term_life": row["term_life"],
                "critical_illness": row["critical_illness"],
                "premium_per_pax": row["premium_per_pax"],
                "total_premium": row["total_premium"]
            })
    return list(pymes.values())

# Obtener seguros de Pyme por su ID 
@app.get("/pymes/{id}", response_model=schemas.PymeOutput)
def get_pyme_with_products(id: int):
    mydb = connect_to_db()
    cursor = mydb.cursor(dictionary=True)
    
    # Obtener los datos de la Pyme
    cursor.execute("SELECT * FROM Pymes WHERE pymesId = %s", (id,))
    pyme = cursor.fetchone()
    
    if not pyme:
        error_code = "ERR0017"
        error_message = "Error, codigo de seguro invalido"
        trace_id = str(uuid.uuid4())
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error-code": error_code, "error-message": error_message, "trace-id": trace_id}
        )
    
    # Obtener los productos asociados a la Pyme
    cursor.execute("SELECT * FROM Products WHERE pymesId = %s", (id,))
    products = cursor.fetchall()
    
    pyme["products"] = products
    mydb.close()
    
    return pyme

# Listar una nueva Pyme
@app.post("/pymes", response_model=schemas.PymeOutput, status_code=status.HTTP_201_CREATED)
def add_pyme(item: schemas.PymeInput):
    mydb = connect_to_db()
    cursor = mydb.cursor()

    # Insertar en la tabla Pymes
    sql = """INSERT INTO Pymes (total_employee, average_age, is_private, bedded, is_sorted_ascending, register_date)
             VALUES (%s, %s, %s, %s, %s, %s)"""
    val = (item.total_employee, item.average_age, item.is_private, item.bedded, item.is_sorted_ascending, item.register_date)
    cursor.execute(sql, val)
    mydb.commit()
    inserted_id = cursor.lastrowid

    # Insertar en la tabla Coverage
    coverage_sql = """INSERT INTO Coverage (outpatient_gp, outpatient_sp, outpatient_dental, personal_accident, term_life, critical_illness)
                      VALUES (%s, %s, %s, %s, %s, %s)"""
    coverage_val = (item.coverage.outpatient_gp, item.coverage.outpatient_sp, item.coverage.outpatient_dental, item.coverage.personal_accident, item.coverage.term_life, item.coverage.critical_illness)
    cursor.execute(coverage_sql, coverage_val)
    mydb.commit()
    coverage_id = cursor.lastrowid

    # Insertar en la tabla Products
    product_sql = """INSERT INTO Products (pymesId, coverageId, product_name, product_options, top_feature, inpatient, outpatient_gp, outpatient_sp, outpatient_dental, personal_accident, term_life, critical_illness, premium_per_pax, total_premium)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    product_val = (inserted_id, coverage_id, None, None, None, None, None, None, None, None, None, None, None, None)
    cursor.execute(product_sql, product_val)
    mydb.commit()

    mydb.close()
    return {"pymesId": inserted_id, **item.dict()}

# Modificar una Pyme por su ID
@app.put("/pymes/{id}", response_model=schemas.PymeOutput)
def update_pyme(id: int, item: schemas.PymeInput):
    mydb = connect_to_db()
    cursor = mydb.cursor()

    # Actualizar la tabla Pymes
    sql = """UPDATE Pymes SET total_employee=%s, average_age=%s, is_private=%s, bedded=%s, is_sorted_ascending=%s, register_date=%s
             WHERE pymesId=%s"""
    val = (item.total_employee, item.average_age, item.is_private, item.bedded, item.is_sorted_ascending, item.register_date, id)
    cursor.execute(sql, val)
    mydb.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pyme not found")
    
    # Actualizar la tabla Coverage
    cursor.execute("SELECT coverageId FROM Products WHERE pymesId=%s", (id,))
    coverage_id = cursor.fetchone()["coverageId"]

    coverage_sql = """UPDATE Coverage SET outpatient_gp=%s, outpatient_sp=%s, outpatient_dental=%s, personal_accident=%s, term_life=%s, critical_illness=%s
                      WHERE coverageId=%s"""
    coverage_val = (item.coverage.outpatient_gp, item.coverage.outpatient_sp, item.coverage.outpatient_dental, item.coverage.personal_accident, item.coverage.term_life, item.coverage.critical_illness, coverage_id)
    cursor.execute(coverage_sql, coverage_val)
    mydb.commit()

    mydb.close()
    return {"pymesId": id, **item.dict()}

# Eliminar una Pyme por su ID
@app.delete("/pymes/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pyme(id: int):
    mydb = connect_to_db()
    cursor = mydb.cursor()

    # Eliminar la cobertura asociada
    cursor.execute("SELECT coverageId FROM Products WHERE pymesId=%s", (id,))
    coverage_id = cursor.fetchone()["coverageId"]
    cursor.execute("DELETE FROM Coverage WHERE coverageId=%s", (coverage_id,))
    
    # Eliminar productos asociados a la Pyme
    cursor.execute("DELETE FROM Products WHERE pymesId = %s", (id,))
    
    # Eliminar la Pyme
    cursor.execute("DELETE FROM Pymes WHERE pymesId = %s", (id,))
    mydb.commit()
    mydb.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pyme not found")
    return {"detail": "Pyme deleted successfully"}