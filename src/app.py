#! /usr/bin/etc  python3
#-*- coding: utf-8 -*-

from flask  import Flask, render_template, jsonify , request
from config import config
from flask_mysqldb import MySQL
from modelos import Sem_Db_Manager


app = Flask(__name__)
conexion = MySQL(app)

@app.route('/')
def index():
    return "HOLA MUNDO DESDE FLASK"

@app.route('/login', methods=["GET"])
def login():
    db = Sem_Db_Manager()
    result=db.login(conexion)
    #print("IMPRIMO RETURN DEL METODO", result)
    if result["mensaje"]=="ERROR":
        return jsonify({"status":False, "codigo":452, "data":"", "mensaje": "ERROR EN LA CONSULTA SQL"})
    elif (result["mensaje"]=="SI"):
        return jsonify({"status": True, "codigo": 200, "data":result["usuarios"], "mensaje": "LISTADO DE USUARIOS"})
    else:
        return jsonify({"status":False, "codigo":453, "data":"","mensaje": "NO HAY USUARIOS EN LA BASE"})
'''     
status=True o False
Codigo = 200 o 400
data = 
mensaje = 
 '''
    

@app.route('/login/<dni>', methods=["GET"])
def busqueda_x_usuario(dni):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM usuarios WHERE dniusuario = {0}".format(dni)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            usuario = {"nombre y apellido":datos[2]+" "+datos[3]}
            return jsonify({"usuario":usuario, "mensaje": "DATOS DEL USUARIO"})
        else:
            return jsonify({"mensaje":"USUARIO NO ENCOTRADO"})
              
    except Exception as ex:
        print(ex)
        return jsonify({"mensaje":"ERROR"})

@app.route('/registrar', methods=['POST'])
def registro_de_usuario():
     #print(request.json)
    try:
        cursor = conexion.connection.cursor()
        sql ="""INSERT INTO usuarios (dniusuario, nomusuario, apeusuario, direusuario, numusuario, pisousuario, deptousuario, localusuario, provusuario, 
            fnacusuario, faltusuario, celusuario, mailusuario, passusuario) 
            VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}')""".format(request.json["dniusuario"],request.json["nomusuario"],request.json["apeusuario"],request.json["direusuario"],request.json["numusuario"],request.json["pisousuario"],request.json["deptousuario"],request.json["localusuario"],request.json["provusuario"],request.json["fnacusuario"],request.json["faltusuario"],request.json["celusuario"],request.json["mailusuario"],request.json["passusuario"])
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({"mensaje":"USUARIO REGISTRADO"})
              
    except Exception as ex:
        print(ex)
        return jsonify({"mensaje":"ERROR"})

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
        return jsonify({"mensaje":"ERROR"})


def pagina_no_encontrada(error):
    return "<h1>LA PAGINA QUE INTENTAS ACCEDER NO EXISTE</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config["desarrollo"])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()