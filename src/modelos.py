#! /usr/bin/etc  python3
#-*- coding: utf-8 -*-

from flask  import render_template, jsonify , request
from config import desarrolloConfig
from flask_mysqldb import MySQL

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
        