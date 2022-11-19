#! /usr/bin/etc  python3
#-*- coding: utf-8 -*-

from flask  import render_template, jsonify , request
from config import desarrolloConfig
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

class Sem_Db_Manager(object):
    
      
    def login(self,conexion):
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
                #print (self.usuarios)
                return {"usuarios":self.usuarios, "mensaje":"SI"}
            else: 
                return {"usuarios":self.usuarios, "mensaje":"NO"}
        except Exception as ex:
            print(ex)
            return  {"usuarios":self.usuarios, "mensaje":"ERROR"}
    
    
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
        
        
        
    def busqueda_usuario(self,conexion):
        try:
            self.cursor = conexion.connection.cursor()
            self.sql = "SELECT * FROM usuarios WHERE dniusuario = {0}".format(request.json["dniusuario"])
            self.cursor.execute(self.sql)
            self.dato = self.cursor.fetchone()
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
    
    
    def busqueda_vehiculo(self,conexion):
        print("ESTOY EN BUSQUEDA VEHICULO")
        try:
            self.cursor = conexion.connection.cursor()
            self.sql = "SELECT * FROM vehiculo WHERE domvehiculo = {0}".format(request.json["domvehiculo"])
            print("IMPRIMO EL SQL: \n", self.sql)
            self.cursor.execute(self.sql)
            conexion.connection.commit()
            self.dato = self.cursor.fetchone()
            if self.dato != None:
                self.vehiculo = {"idvehiculo":self.dato[0], "domvehiculo":self.dato[1],"marvehiculo":self.dato[2], "tipovehiculo":self.dato[3]}
                return {"vehiculo":self.usuario, "mensaje":"SI"}
                
            else:
                return {"vehiculo":"", "mensaje":"NO"}
        except Exception as ex:
            print(ex)
            return  {"vehiculo":"", "mensaje":"ERROR"}
        
        
        
    def registro_usuario(self,conexion):
        self.hay_usuario = self.busqueda_usuario(conexion)
        if (self.hay_usuario["mensaje"]!="ERROR"):
            try:
                self.cursor = conexion.connection.cursor()
                self.passhashed=generate_password_hash(request.json["passusuario"])
                self.sql ="""INSERT INTO usuarios (dniusuario, nomusuario, apeusuario, direusuario, numusuario, pisousuario, deptousuario, localusuario, provusuario, 
                    fnacusuario, faltusuario, celusuario, mailusuario, passusuario) 
                    VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}')""".format(request.json["dniusuario"],request.json["nomusuario"],request.json["apeusuario"],request.json["direusuario"],request.json["numusuario"],request.json["pisousuario"],request.json["deptousuario"],request.json["localusuario"],request.json["provusuario"],request.json["fnacusuario"],request.json["faltusuario"],request.json["celusuario"],request.json["mailusuario"], self.passhashed)
                self.cursor.execute(self.sql)
                conexion.connection.commit()
                self.sql = "SELECT * FROM usuarios WHERE dniusuario = {0}".format(request.json["dniusuario"])
                self.cursor.execute(self.sql)
                self.dato = self.cursor.fetchone()
                if self.dato != None:
                    self.usuario = {"id":self.dato[0], "dni":self.dato[1],"nombre":self.dato[2], "apellido":self.dato[3],"direccion":self.dato[4],"numero":self.dato[5],"piso":self.dato[6],"depto":self.dato[7],"local":self.dato[8],"prov":self.dato[9],"fnac":self.dato[10],"falta":self.dato[11],"celu":self.dato[12],"mail":self.dato[13]}
                return {"usuarios":self.usuario, "mensaje":"SI"}
                    
            except Exception as ex:
                print(ex)
                return  {"usuarios":"", "mensaje":"ERROR"}
            
        else:
            return {"usuarios":"", "mensaje":"HAY USUARIO"}
        
        
    def registro_vehiculo(self,conexion):
        self.hay_vehiculo = self.busqueda_vehiculo(conexion)
        if (self.hay_vehiculo["mensaje"]!="ERROR"):
            if (self.hay_vehiculo["mensaje"]=="NO"):
                try:
                    self.cursor = conexion.connection.cursor()
                    self.sql ="""INSERT INTO vehiculo (domvehiculo, marvehiculo, tipovehiculo) 
                        VALUES ('{0}','{1}','{2}')""".format(request.json["domvehiculo"],request.json["marvehiculo"],request.json["tipovehiculo"])
                    self.cursor.execute(self.sql)
                    conexion.connection.commit()
                    self.sql = "SELECT * FROM vehiculo WHERE domvehiculo = {0}".format(request.json["domvehiculo"])
                    self.cursor.execute(self.sql)
                    conexion.connection.commit()
                    self.dato = self.cursor.fetchone()
                    # COMPRUEBA QUE SE HAYA REALIZADO EL INGRESO DEL NUEVO REGISTRO
                    if self.dato != None:
                        self.vehiculo = {"idvehiculo":self.dato[0], "domvehiculo":self.dato[1],"marvehiculo":self.dato[2], "tipovehiculo":self.dato[3]}
                        return {"vehiculos":self.vehiculo, "mensaje":"SI"}
                
                except Exception as ex:
                    print(ex)
                    return  {"vehiculos":"", "mensaje":"ERROR"}
            else:
                return {"vehiculos":"", "mensaje":"HAY DOMINIO"}
            
        else:
            return {"vehiculos":"", "mensaje":"ERROR"}
                    
                
      
 
        