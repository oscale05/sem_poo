#!/usr/bin/etc  python3
#-*- coding: utf-8 -*-

from flask  import Flask, render_template, jsonify , request
from config import config
import db

import modelos
from modelos import Sem_Db_Manager


app = Flask(__name__)


@app.route('/')
def index():
    return "HOLA MUNDO DESDE FLASK"


@app.route('/login', methods=["POST"])
def login():
    dbase = Sem_Db_Manager()
    result= dbase.login()
    if result["mensaje"]=="ERROR":
        return jsonify({"status":False, "codigo":452, "data":"", "mensaje": "ERROR EN LA CONSULTA SQL"}),452

    elif (result["mensaje"]=="NOPASS"):
        return jsonify({"status": False, "codigo": 454, "data":"", "mensaje": "USUARIO Y PASSWORD NO COINCIDEN"}),454

    elif (result["mensaje"]=="SI"):
        return jsonify({"status": True, "codigo": 200, "data":result["usuarios"], "mensaje": "DATOS DE USUARIO ENCONTRADOS"})
    else:
        return jsonify({"status":False, "codigo":453, "data":"","mensaje": "EL USUARIO BUSCADO NO SE ENCUENTRA EN BASE"}),453
    




@app.route('/listado_reservas', methods=["GET"])
def listado_reservas():
    db = Sem_Db_Manager()
    result=db.list_reservas()
    #print("IMPRIMO RETURN DEL METODO", result)
    if result["mensaje"]=="ERROR":
        return jsonify({"status":False, "codigo":452, "data":"", "mensaje": "ERROR EN LA CONSULTA SQL"}),452
    elif (result["mensaje"]=="SI"):
        ''' print(result)
        print(type(result)) '''
        return jsonify({"status": True, "codigo": 200, "data":result["usuarios"], "mensaje": "LISTADO DE USUARIOS"})
    else:
        return jsonify({"status":False, "codigo":453, "data":"","mensaje": "NO HAY USUARIOS EN LA BASE"}),453


@app.route('/usuario', methods=["POST"])
def busqueda_x_usuario():
    db = Sem_Db_Manager()
    result= db.busqueda_usuario()
    if result["mensaje"]=="ERROR":
        return jsonify({"status":False, "codigo":452, "data":"", "mensaje": "ERROR EN LA CONSULTA SQL"}),452

    elif (result["mensaje"]=="NOPASS"):
        return jsonify({"status": False, "codigo": 454, "data":"", "mensaje": "USUARIO Y PASSWORD NO COINCIDEN"}),454

    elif (result["mensaje"]=="SI"):
        return jsonify({"status": True, "codigo": 200, "data":result["usuarios"], "mensaje": "DATOS DE USUARIO ENCONTRADOS"})
    else:
        return jsonify({"status":False, "codigo":453, "data":"","mensaje": "EL USUARIO BUSCADO NO SE ENCUENTRA EN BASE"}),453
    
    
@app.route('/registrar_usuario', methods=['POST'])
def registro_de_usuario():
    dbase = Sem_Db_Manager()
    usuario= dbase.registro_usuario()
    print("IMPRIMO USUARIO, ", usuario)
    
    vehiculo= dbase.registro_vehiculo()
    if (usuario["mensaje"]=="ERROR" and vehiculo["mensaje"]=="ERROR"):
        return jsonify({"status":False, "codigo":452, "data":"", "mensaje": "ERROR EN LA CONSULTA SQL"}), 452

    elif (vehiculo["mensaje"]=="SI"):
        return jsonify({"status": True, "codigo": 200, "data":vehiculo["vehiculos"], "mensaje": "REGISTRO EXITOSO"})
    
    elif (usuario["mensaje"]=="HAY USUARIO" and vehiculo["mensaje"]=="HAY DOMINIO"):
        return jsonify({"status": False, "codigo": 456, "data":"", "mensaje": "REGISTRO YA EXISTENTE"}),456
    
    elif (vehiculo["mensaje"]=="MAXIMO"):
        return jsonify({"status": False, "codigo": 458, "data":"", "mensaje": "USUARIO YA TIENE 5 VEHICULOS REGISTRADOS"}),458
    
    else:
        return jsonify({"status":False, "codigo":455, "data":"","mensaje": "USUARIO NO PUEDO REGISTRARSE"}), 455


    
     
     
@app.route('/eliminar_reg_vehiculo', methods=['POST'])
def eliminacion_reg_vehiculo():
    dbase = Sem_Db_Manager()
    result= dbase.eliminar_reg_vehiculo()
    if result["mensaje"]=="ERROR":
        return jsonify({"status":False, "codigo":452, "data":"", "mensaje": "ERROR EN LA CONSULTA SQL"}), 452

    elif (result["mensaje"]=="SI"):
        return jsonify({"status": True, "codigo": 200, "data":result["vehiculos"], "mensaje": "VEHICULO ELIMINADO"})
    
    elif (result["mensaje"]=="ULTIMO"):
        return jsonify({"status": True, "codigo": 200, "data":result["vehiculos"], "mensaje": "ULTIMO REGISTRO VEHICULO ELIMINADO"})
    
    
    else:
        return jsonify({"status":False, "codigo":455, "data":"","mensaje": "DOMINIO NO PUDO ELIMINARSE"}), 455
     
        
    

@app.route("/eliminar", methods=["POST"])
def eliminar_usuario():
    dbase = Sem_Db_Manager()
    usuario= dbase.elimino_usuario()
    print("IMPRIMO USUARIO, ", usuario)

    if (usuario["mensaje"]=="ERROR" and usuario["mensaje"]=="ERROR"):
        return jsonify({"status":False, "codigo":452, "data":"", "mensaje": "ERROR EN LA CONSULTA SQL"}), 452

    elif (vehiculo["mensaje"]=="SI"):
        return jsonify({"status": True, "codigo": 200, "data":vehiculo["vehiculos"], "mensaje": "REGISTRO EXITOSO"})
    
    elif (usuario["mensaje"]=="HAY USUARIO" and vehiculo["mensaje"]=="HAY DOMINIO"):
        return jsonify({"status": False, "codigo": 456, "data":"", "mensaje": "REGISTRO YA EXISTENTE"}),456
    
    elif (vehiculo["mensaje"]=="MAXIMO"):
        return jsonify({"status": False, "codigo": 458, "data":"", "mensaje": "USUARIO YA TIENE 5 VEHICULOS REGISTRADOS"}),458
    
    else:
        return jsonify({"status":False, "codigo":455, "data":"","mensaje": "USUARIO NO PUEDO REGISTRARSE"}), 455


    
''' @app.route("/actualizar/<dni>", methods=["PUT"])
def actualizar_usuario(dni):
    try:
        cursor = conexion.connection.cursor()
        sql = """UPDATE usuarios SET direusuario = '{0}', numusuario = '{1}' 
        WHERE dniusuario = {2}""".format(request.json["direusuario"], request.json["numusuario"], dni)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({"mensaje":"USUARIO MODIFICADO"})
              
    except Exception as ex:
        print(ex)
        return jsonify({"mensaje":"ERROR"}) '''


def pagina_no_encontrada(error):
    return "<h1>LA PAGINA QUE INTENTAS ACCEDER NO EXISTE</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config["desarrollo"])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()