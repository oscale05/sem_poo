#!/usr/bin/python 
import mariadb 

conn = mariadb.connect(
    user="dev",
    password="Larisa_2305",
    host="localhost",
    database="sem")
cur = conn.cursor() 
 
#retrieving information 
dni = "22324987" 
cur.execute("SELECT * FROM usuarios WHERE dniusuario=?", (dni,)) 

for apeusuario in cur: 
    print (f"Apellido: {apeusuario[1]}")
    
#insert information 
try: 
    cur.execute("INSERT INTO vehiculo (domvehiculo, marvehiculo, tipovehiculo) VALUES (?, ?, ?)", ("NVK855","CHEVROLET", "SEDAN 4")) 
except mariadb.Error as e: 
    print(f"Error: {e}")

conn.commit() 
print(f"Last Inserted ID: {cur.lastrowid}")
    
conn.close()