# from flask import Flask
# from flask import render_template, jsonify, request, redirect, url_for
# import json
# from connectiondb import connect_db, get_list
# app = Flask(__name__)


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     """Retorna la pagina index."""
#     print("OK")
#     if(request.method == 'GET'):
#         con = connect_db()

#         lista = get_list("personajes")
#     return render_template('/index.html', datos=lista)

# @app.route('/cargar')
# def cargar():
#     dic = {'nombre': '', 'aparicion': '', 'biografia': '', 'personaje': ''}
#     return render_template('/cargar.html', documento=dic)


# @app.route('/about')
# def about():
#     """Retorna la pagina about."""
#     return render_template('/about.html', msj="About de la pagina")



# if __name__ == '__main__':
#     app.run(host='web-app-flask', port='5000', debug=True)

# app.py
from flask import Flask, render_template, request, jsonify
from connectiondb import init_episodes, listar_capitulos, reservar_capitulo, confirmar_pago

app = Flask(__name__)

@app.route('/')
def index():
    init_episodes()  # Cargar datos iniciales si no están
    lista = listar_capitulos()
    return render_template("index.html", datos=lista)

@app.route('/alquilar/<id_capitulo>', methods=['POST'])
def alquilar(id_capitulo):
    if reservar_capitulo(id_capitulo):
        return jsonify({"msg": "Capítulo reservado por 4 minutos."}), 200
    return jsonify({"msg": "No disponible."}), 400

@app.route('/confirmar_pago', methods=['POST'])
def confirmar():
    datos = request.get_json()
    if confirmar_pago(datos["id"], datos["precio"]):
        return jsonify({"msg": "Pago confirmado. Alquilado por 24 hs."}), 200
    return jsonify({"msg": "No se pudo confirmar el pago."}), 400

if __name__ == '__main__':
    app.run(host='web-app-flask', port='5000', debug=True)


