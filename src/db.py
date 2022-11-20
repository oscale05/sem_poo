#! /usr/bin/etc  python3
#-*- coding: utf-8 -*-
import mariadb 

def conexion_db():
    conexion = mariadb.connect(
        user="dev",
        password="Larisa_2305",
        host="localhost",
        database="sem")
    return conexion.cursor()
        
    
