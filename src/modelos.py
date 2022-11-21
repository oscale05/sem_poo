#! /usr/bin/etc  python3
#-*- coding: utf-8 -*-

from flask  import render_template, jsonify , request
import config
import db
from werkzeug.security import generate_password_hash, check_password_hash

class Sem_Db_Manager(object):
    
      
    def login(self):
        try:
            self.conn = db.conexion_db()
            self.cursor = self.conn.cursor()
            self.cursor.execute("SELECT * FROM usuarios WHERE dniusuario = %s", (request.json["dniusuario"],))   
            self.conn.commit()
            self.dato = self.cursor.fetchone()
            self.conn.close()
            if self.dato != None:
                self.usuario = {"id":self.dato[0], "dni":self.dato[1],"nombre":self.dato[2], "apellido":self.dato[3],"direccion":self.dato[4],"numero":self.dato[5],"piso":self.dato[6],"depto":self.dato[7],"local":self.dato[8],"prov":self.dato[9],"fnac":self.dato[10],"falta":self.dato[11],"celu":self.dato[12],"mail":self.dato[13]}
                if(check_password_hash(self.dato[14], request.json["password"])):
                    return {"usuarios":self.usuario, "mensaje":"SI"}
                else:
                    return {"usuarios":self.usuario, "mensaje":"NOPASS"}
            else:
                return {"usuarios":"", "mensaje":"NO"}
        except Exception as ex:
            print(ex)
            return  {"usuarios":"", "mensaje":"ERROR"}
        
        
      
    
    def list_reservas(self,conexion):
        try:
            self.cursor = conexion.connection.cursor()
            self.sql = "SELECT * FROM usuarios"
            self.cursor.execute(self.sql)
            self.datos = self.cursor.fetchall()
            if (self.datos != None):
                self.usuarios = []
                for dato in self.datos:
                    #self.usuario = {"nombre y apellido":dato[2]+" "+dato[3]}
                    self.usuario = {"id":dato[0], "dni":dato[1],"nombre":dato[2], "apellido":dato[3],"direccion":dato[4],"numero":dato[5],"piso":dato[6],"depto":dato[7],"local":dato[8],"prov":dato[9],"fnac":dato[10],"falta":dato[11],"celu":dato[12],"mail":dato[13]}
                    self.usuarios.append(self.usuario)
                    #print (self.usuario)
                print ("IMPRIMO LO QUE ME TRAIGO DE LA BASE",self.usuarios)
                return {"usuarios":self.usuarios, "mensaje":"SI"}
            else: 
                return {"usuarios":"", "mensaje":"NO"}
        except Exception as ex:
            print(ex)
            return  {"usuarios":"", "mensaje":"ERROR"}
        
        
        
    def busqueda_usuario(self):
        try:
            self.conn = db.conexion_db()
            self.cursor = self.conn.cursor()
            self.cursor.execute("SELECT * FROM usuarios WHERE dniusuario = %s", (request.json["dniusuario"],))
            self.conn.commit()
            self.dato = self.cursor.fetchone()
            self.conn.close()
            if self.dato != None:
                return {"usuarios":self.dato, "mensaje":"SI"}
                ''' self.usuario = {"id":self.dato[0], "dni":self.dato[1],"nombre":self.dato[2], "apellido":self.dato[3],"direccion":self.dato[4],"numero":self.dato[5],"piso":self.dato[6],"depto":self.dato[7],"local":self.dato[8],"prov":self.dato[9],"fnac":self.dato[10],"falta":self.dato[11],"celu":self.dato[12],"mail":self.dato[13]}
                if(check_password_hash(self.dato[14], request.json["password"])):
                    return {"usuarios":self.usuario, "mensaje":"SI"}
                else:
                    return {"usuarios":self.usuario, "mensaje":"NOPASS"} '''
            else:
                return {"usuarios":"", "mensaje":"NO"}
        except Exception as ex:
            print(ex)
            return  {"usuarios":"", "mensaje":"ERROR"}
    
    
    def busqueda_vehiculo(self):
        
        try:
            self.conn = db.conexion_db()
            self.cursor = self.conn.cursor()
            self.cursor.execute("SELECT * FROM vehiculo WHERE domvehiculo = %s", (request.json["domvehiculo"],))
            self.conn.commit()
            self.dato = self.cursor.fetchone()
            self.conn.close()
            print ("IMPRIMO DATOS DEL VEHICULOS DESDE BUSQUEDA ", self.dato)
            if self.dato != None:
                self.vehiculo = {"idvehiculo":self.dato[0], "domvehiculo":self.dato[1],"marvehiculo":self.dato[2], "tipovehiculo":self.dato[3]}
                return {"vehiculos":self.vehiculo, "mensaje":"SI"}
                
            else:
                return {"vehiculos":"", "mensaje":"NO"}
        except Exception as ex:
            print(ex)
            return  {"vehiculos":"", "mensaje":"ERROR"}
        
        
    #       DEBO VERIFICAR QUE NO EXISTA EN LA TABLA USUARIO_VEHICULO UN REGISTRO
    #       CON MISMO USUARIO Y MISMO DOMINIO
    
    def busqueda_usuario_vehiculo(self):
        
        try:
            self.conn = db.conexion_db()
            self.cursor = self.conn.cursor()
            self.cursor.execute("SELECT COUNT(*) FROM usuario_vehiculo WHERE id_dniusuario = %s", (request.json["dniusuario"],))
            self.conn.commit()
            self.dato = self.cursor.fetchone()
            print("IMPRIMO LA CANTIDAD DE REGISTROS QUE HAY EN LA TABLA USUARIO_VEHICULO PARA UN USUARIO DETERMINADO, ",self.dato[0])
            if self.dato[0] < 5: 
                self.cursor.execute("SELECT * FROM usuario_vehiculo WHERE id_dniusuario = %s AND id_domvehiculo = %s", (request.json["dniusuario"],request.json["domvehiculo"],))
                self.conn.commit()
                self.dato = self.cursor.fetchone()
                self.conn.close()
                if self.dato != None:
        
                    return {"vehiculos":"", "mensaje":"SI"}
                    
                else:
                    return {"vehiculos":"", "mensaje":"NO"}
            
            else:
                return {"vehiculos":"", "mensaje":"MAXIMO"}
        except Exception as ex:
            print(ex)
            return  {"vehiculos":"", "mensaje":"ERROR"}
    
    
    def busqueda_eliminacion_reg_usuario_vehiculo(self):
        #   AVERGUO SI ES EL ULTIMO REGISTRO DE ESE DOMINIO EN USUARIO_VEHICULO
        try:
            self.conn = db.conexion_db()
            self.cursor = self.conn.cursor()
            self.cursor.execute("SELECT COUNT(*) FROM usuario_vehiculo WHERE id_domvehiculo = %s", (request.json["domvehiculo"],))
            self.conn.commit()
            self.dato = self.cursor.fetchone()
            print("IMPRIMO LA CANTIDAD DE REGISTROS QUE HAY EN LA TABLA USUARIO_VEHICULO PARA UN VEHICULO DETERMINADO, ",self.dato[0])
            if self.dato[0] == 1: 
                return {"vehiculos":"", "mensaje":"SI"}
                    
            else:
                return {"vehiculos":"", "mensaje":"NO"}
            
            
        except Exception as ex:
            print(ex)
            return  {"vehiculos":"", "mensaje":"ERROR"}
       
        
        
    def registro_usuario(self):
        self.hay_usuario = self.busqueda_usuario()
        if (self.hay_usuario["mensaje"]=="NO"):
            try:
                self.conn = db.conexion_db()
                self.cursor = self.conn.cursor()
                self.passhashed=generate_password_hash(request.json["passusuario"])
                self.sql ="""INSERT INTO usuarios (dniusuario, nomusuario, apeusuario, direusuario, numusuario, pisousuario, deptousuario, localusuario, provusuario, 
                    fnacusuario, faltusuario, celusuario, mailusuario, passusuario) 
                    VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}')""".format(request.json["dniusuario"],request.json["nomusuario"],request.json["apeusuario"],request.json["direusuario"],request.json["numusuario"],request.json["pisousuario"],request.json["deptousuario"],request.json["localusuario"],request.json["provusuario"],request.json["fnacusuario"],request.json["faltusuario"],request.json["celusuario"],request.json["mailusuario"], self.passhashed)
                self.cursor.execute(self.sql)
                self.conn.commit()
                self.conn.close()
                
                return {"usuarios":"", "mensaje":"SI"}
                    
            except Exception as ex:
                print(ex)
                return  {"usuarios":"", "mensaje":"ERROR"}
        
        elif self.hay_usuario["mensaje"]=="SI":
            return {"usuarios":"", "mensaje":"HAY USUARIO"}
            
        else:
            return {"usuarios":"", "mensaje":"ERROR"}
        
     
        
    def registro_vehiculo(self):
        self.hay_usuario_vehiculo = self.busqueda_usuario_vehiculo()
        print ("IMPRIMO SELF.HAY_USUARIO_VEHICULO, ", self.hay_usuario_vehiculo["mensaje"])
        if (self.hay_usuario_vehiculo["mensaje"]!="ERROR"):
            if (self.hay_usuario_vehiculo["mensaje"]!="MAXIMO"):
            
                if (self.hay_usuario_vehiculo["mensaje"]=="NO"):
                    self.hay_vehiculo = self.busqueda_vehiculo()
                    print("IMPRIMO SELF.HAY_VEHICULO ", self.hay_vehiculo)
                    if (self.hay_vehiculo["mensaje"]!="ERROR"):
                        if (self.hay_vehiculo["mensaje"]=="NO"):
                            #   INSERT DE NUEVO REGISTRO TANTO EN TABLA VEHICULO COMO EN USUARIO_VEHICULO
                            try:
                                self.conn = db.conexion_db()
                                self.cursor = self.conn.cursor()
                                self.cursor.execute("INSERT INTO vehiculo (domvehiculo, marvehiculo, tipovehiculo) VALUES (?, ?, ?)", (request.json["domvehiculo"],request.json["marvehiculo"],request.json["tipovehiculo"],))
                                self.conn.commit()
                                self.idvehiculo = self.cursor.lastrowid
                                self.cursor.execute("SELECT idusuario  FROM usuarios WHERE dniusuario = %s ", (request.json["dniusuario"],))
                                self.conn.commit()
                                self.dato = self.cursor.fetchone()
                                print("IMPRIMO EL VALOR DE DATO, ", self.dato)
                                self.cursor.execute("INSERT INTO usuario_vehiculo (id_usuario, id_dniusuario, id_vehiculo, id_domvehiculo) VALUES (?, ?, ?, ?)", (self.dato[0],request.json["dniusuario"],self.idvehiculo, request.json["domvehiculo"],))
                                self.conn.commit()
                                self.conn.close()
                                
                                return {"vehiculos":"", "mensaje":"SI"}
                            
                            except Exception as ex:
                                print(ex)
                                return  {"vehiculos":"", "mensaje":"ERROR"}
                        else:
                    
                            try:
                                self.conn = db.conexion_db()
                                self.cursor = self.conn.cursor()
                                self.cursor.execute("SELECT idvehiculo  FROM vehiculo WHERE domvehiculo = %s ", (request.json["domvehiculo"],))
                                self.conn.commit()
                                self.dato = self.cursor.fetchone()
                                print("IMPRIMO EL VALOR DEL IDVEHICULO, ", self.dato[0])
                                self.idvehiculo = self.dato[0]
                                self.cursor.execute("SELECT idusuario  FROM usuarios WHERE dniusuario = %s ", (request.json["dniusuario"],))
                                self.conn.commit()
                                self.dato = self.cursor.fetchone()
                                print("ESTOY INSERTANDO EN USUARIO_VEHICULO UN DOMINIO QUE YA TENGO EN VEHICULO IMPRIMO EL VALOR DE DATO, ", self.dato)
                                self.cursor.execute("INSERT INTO usuario_vehiculo (id_usuario, id_dniusuario, id_vehiculo, id_domvehiculo) VALUES (?, ?, ?, ?)", (self.dato[0],request.json["dniusuario"],self.idvehiculo, request.json["domvehiculo"],))
                                self.conn.commit()
                                self.conn.close()
                                
                                return {"vehiculos":"", "mensaje":"SI"}
                            except Exception as ex:
                                print(ex)
                                return  {"vehiculos":"", "mensaje":"ERROR"}
                    else:
                        return {"vehiculos":"", "mensaje":"ERROR"}
                else:
                    return {"vehiculos":"", "mensaje":"HAY DOMINIO"}
            else:
                   return {"vehiculos":"", "mensaje":"MAXIMO"} 
            
        else:
            return {"vehiculos":"", "mensaje":"ERROR"}
                    
    def eliminar_reg_vehiculo(self):
        self.hay_reg_usuario_vehiculo = self.busqueda_eliminacion_reg_usuario_vehiculo()
        print ("IMPRIMO SELF.HAY__REG_USUARIO_VEHICULO, ", self.hay_reg_usuario_vehiculo["mensaje"])
        if (self.hay_reg_usuario_vehiculo["mensaje"]!="ERROR"):
            
            
            if (self.hay_reg_usuario_vehiculo["mensaje"]=="NO"):
            #   DELETE EL REGISTRO SOLO DE USUARIO_VEHICULO 
                try:
                    self.conn = db.conexion_db()
                    self.cursor = self.conn.cursor()
                    self.sql=("DELETE FROM usuario_vehiculo WHERE id_dniusuario = s% AND  id_domvehiculo = s%")
                    reg =(request.json["dniusuario"],request.json["domvehiculo"],)
                    print("ESTOY IMPRIMIENDO EL REG, ", reg)
                    self.cursor.execute(self.sql, reg)
                    self.conn.commit()
                    self.conn.close()
                    return {"vehiculos":"", "mensaje":"SI"}
                
                except Exception as ex:
                    print(ex)
                    return  {"vehiculos":"", "mensaje":"ERROR"}
            else:
            #   DELETE EL REGISTRO DE VEHICULO Y DE USUARIO_VEHICULO 
                try:
                    print ("ESTOY ACA")
                    self.conn = db.conexion_db()
                    self.cursor = self.conn.cursor()
                    self.cursor.execute=("DELETE FROM usuario_vehiculo WHERE id_dniusuario = s% AND  id_domvehiculo =s%", (request.json["dniusuario"],request.json["domvehiculo"],))
                    self.conn.commit()
                    domvehiculo = request.json["domvehiculo"]
                    self.cursor.execute=("DELETE FROM vehiculo WHERE id_domvehiculo = s% ", domvehiculo)
                    self.conn.commit()
                    self.conn.close()
                    
                    return {"vehiculos":"", "mensaje":"ULTIMO"}
                except Exception as ex:
                    print(ex)
                    return  {"vehiculos":"", "mensaje":"ERROR"}
                
       
          
            
        else:
            return {"vehiculos":"", "mensaje":"ERROR"}            
      
 
        