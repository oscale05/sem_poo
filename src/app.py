#!/usr/bin/etc  python3
#-*- coding: utf-8 -*-

from flask  import Flask, render_template, jsonify , request
from config import config
import db


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
    db = Sem_Db_Manager()
    result= db.registro_usuario()
    if result["mensaje"]=="ERROR":
        return jsonify({"status":False, "codigo":452, "data":"", "mensaje": "ERROR EN LA CONSULTA SQL"}), 452

    elif (result["mensaje"]=="SI"):
        return jsonify({"status": True, "codigo": 200, "data":result["usuarios"], "mensaje": "USUARIO REGISTRADO"})
    
    elif (result["mensaje"]=="HAY USUARIO"):
        return jsonify({"status": False, "codigo": 456, "data":"", "mensaje": "USUARIO YA EXISTENTE"}),456
    
    else:
        return jsonify({"status":False, "codigo":455, "data":"","mensaje": "USUARIO NO PUEDO REGISTRARSE"}), 455
     

@app.route('/registrar_vehiculo', methods=['POST'])
def registro_de_vehiculo():
    db = Sem_Db_Manager()
    result= db.registro_vehiculo()
    if result["mensaje"]=="ERROR":
        return jsonify({"status":False, "codigo":452, "data":"", "mensaje": "ERROR EN LA CONSULTA SQL"}), 452

    elif (result["mensaje"]=="SI"):
        return jsonify({"status": True, "codigo": 200, "data":result["vehiculo"], "mensaje": "VEHI REGISTRADO"})
    
    elif (result["mensaje"]=="HAY VEHICULO"):
        return jsonify({"status": False, "codigo": 456, "data":"", "mensaje": "DOMINIO YA EXISTENTE"}),456
    
    else:
        return jsonify({"status":False, "codigo":455, "data":"","mensaje": "DOMINIO NO PUDO REGISTRARSE"}), 455
     
    
    
''' 
@app.route("/eliminar/<dni>", methods=["DELETE"])
def eliminar_usuario(dni):
    try:
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM usuarios WHERE dniusuario = {0}".format(dni)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({"mensaje":"USUARIO ELIMINADO"})
              
    except Exception as ex:
        print(ex)
        return jsonify({"mensaje":"ERROR"})
    
@app.route("/actualizar/<dni>", methods=["PUT"])
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