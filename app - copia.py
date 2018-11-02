#!/usr/bin/env python
import csv
from funciones import chequeoerror
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_bootstrap import Bootstrap
# from flask_moment import Moment
from flask_script import Manager
from forms import LoginForm, SaludarForm, RegistrarForm

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
# moment = Moment(app)

app.config['SECRET_KEY'] = 'un string que funcione como llave'

@app.route('/')
def index():
##### AGREGADO POR PEKE
    error = chequeoerror()
    if error:
        return render_template('error.html', error=error)
##### AGREGADO POR PEKE

    return render_template('index.html', fecha_actual=datetime.utcnow())


@app.route('/saludar', methods=['GET', 'POST'])
def saludar():
    formulario = SaludarForm()
    if formulario.validate_on_submit():
        print(formulario.usuario.name)
        return redirect(url_for('saludar_persona', usuario=formulario.usuario.data))
    return render_template('saludar.html', form=formulario)


@app.route('/saludar/<usuario>')
def saludar_persona(usuario):
    return render_template('usuarios.html', nombre=usuario)


@app.errorhandler(404)
def no_encontrado(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def error_interno(e):
    return render_template('500.html'), 500


@app.route('/ingresar', methods=['GET', 'POST'])
def ingresar():
##### AGREGADO POR PEKE
    error = chequeoerror()
    if error:
        return render_template('error.html', error=error)
##### AGREGADO POR PEKE

    formulario = LoginForm()
    if formulario.validate_on_submit():
        with open('usuarios') as archivo:
            archivo_csv = csv.reader(archivo)
            registro = next(archivo_csv)
            while registro:
                if formulario.usuario.data == registro[0] and formulario.password.data == registro[1]:
                    flash('Bienvenido')
                    session['username'] = formulario.usuario.data
              ##### AGREGADO POR SEBASTIAN #####

                    with open('ventas.csv','r') as archivo:
                        tablaorden = ["CODIGO","PRODUCTO","CLIENTE","PRECIO","CANTIDAD"]
                        tablacsv = csv.DictReader(archivo)

                        cant = 10
                        tabla = []
                        tablafinal = []
                        for line in tablacsv:
                            tabla.append(line)

                        for fila in range(len(tabla)):
                            tablafinal.append([])
                            for columna in range(len(tablaorden)):
                                tablafinal[fila].append(tabla[fila][tablaorden[columna]])

                        x = tablaorden.index("PRECIO")
                        for i in range(len(tablafinal)):
                            tablafinal[i][x] = "$"+str(tablafinal[i][x])
  
            ##### AGREGADO POR SEBASTIAN #####
                        return render_template('ingresado.html', usuario=formulario.usuario.data, titulo=tablaorden, tabla=tablafinal[-cant:])
                registro = next(archivo_csv, None)
            else:
                flash('Revisá nombre de usuario y contraseña')
                return redirect(url_for('ingresar'))
    return render_template('login.html', formulario=formulario)


@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
##### AGREGADO POR PEKE
    error = chequeoerror()
    if error:
        return render_template('error.html', error=error)
##### AGREGADO POR PEKE

    formulario = RegistrarForm()
    if formulario.validate_on_submit():
        if formulario.password.data == formulario.password_check.data:
            with open('usuarios', 'a+') as archivo:
                archivo_csv = csv.writer(archivo)
                registro = [formulario.usuario.data, formulario.password.data]
                archivo_csv.writerow(registro)
            flash('Usuario creado correctamente')
            return redirect(url_for('ingresar'))
        else:
            flash('Las passwords no matchean')
    return render_template('registrar.html', form=formulario)


@app.route('/secret', methods=['GET'])
def secreto():
    if 'username' in session:
        return render_template('private.html', username=session['username'])
    else:
        return render_template('sin_permiso.html')


@app.route('/logout', methods=['GET'])
def logout():
    if 'username' in session:
        session.pop('username')
        return render_template('logged_out.html')
    else:
        return redirect(url_for('index'))

########## AGREGADO POR PEKE

@app.route('/ultvent')
def ultvent():
##### AGREGADO POR PEKE
    error = chequeoerror()
    if error:
        return render_template('error.html', error=error)
##### AGREGADO POR PEKE
    if 'username' not in session:
        return redirect(url_for('ingresar'))

    with open('ventas.csv','r') as archivo:
        tablaorden = ["CODIGO","PRODUCTO","CLIENTE","PRECIO","CANTIDAD"]
        tablacsv = list(csv.DictReader(archivo))

        cant = 20
        tabla = []
        tablafinal = []
        for line in tablacsv:
            tabla.append(line)

        for fila in range(len(tabla)):
            tablafinal.append([])
            for columna in range(len(tablaorden)):
                tablafinal[fila].append(tabla[fila][tablaorden[columna]])

        x = tablaorden.index("PRECIO")
        for i in range(len(tablafinal)):
            tablafinal[i][x] = "$"+str(tablafinal[i][x])

        return render_template('ultvent.html', titulo=tablaorden, tabla=tablafinal[-cant:])

@app.route('/clienbus')
def clienbus():
##### AGREGADO POR PEKE
    error = chequeoerror()
    if error:
        return render_template('error.html', error=error)
##### AGREGADO POR PEKE
    if 'username' not in session:
        return redirect(url_for('index'))
    
    return render_template('clienbus.html')

@app.route('/clientes', methods=["POST" , "GET"])
def clientes():
##### AGREGADO POR PEKE
    error = chequeoerror()
    if error:
        return render_template('error.html', error=error)
##### AGREGADO POR PEKE
    if 'username' not in session:
        return redirect(url_for('ingresar'))

    if request.method == "POST":
        filtro = request.form['nombrecliente']
        if len(filtro) < 3:
            return render_template('clienbus.html', error=1)
        with open('ventas.csv','r') as archivo:
            tablacsv = csv.DictReader(archivo)
            listadoclientes = []

            for linea in tablacsv:
                if filtro.lower() in linea["CLIENTE"].lower():
                    listadoclientes.append(linea["CLIENTE"])

            listadoclientes = list(set(listadoclientes))

            if len(listadoclientes) == 0:
                return render_template('clienbus.html', clie=listadoclientes, lista=0)

            elif len(listadoclientes) == 1:
                return redirect(url_for('clientabla', filtro=listadoclientes[0]))

            return render_template('clienbus.html', clie=listadoclientes, lista=1)

@app.route('/clientabla/<filtro>')
def clientabla(filtro):
##### AGREGADO POR PEKE
    error = chequeoerror()
    if error:
        return render_template('error.html', error=error)
##### AGREGADO POR PEKE
    if 'username' not in session:
        return redirect(url_for('ingresar'))

    with open('ventas.csv','r') as archivo:
        tablacsv = csv.DictReader(archivo)

        gasto = 0
        tabla = []
        tablafinal = []
        tablaorden = ["CODIGO","PRODUCTO","CLIENTE","PRECIO","CANTIDAD"]
        nombre = filtro.replace("%20", " ")

        for line in tablacsv:
            if line["CLIENTE"] == nombre:
                tabla.append(line)

        for fila in range(len(tabla)):
            tablafinal.append([])
            for columna in range(len(tablaorden)):
                tablafinal[fila].append(tabla[fila][tablaorden[columna]])

        for precio in range(len(tabla)):
            gasto = gasto + (int(tabla[precio]["PRECIO"])*int(tabla[precio]["CANTIDAD"]))

        x = tablaorden.index("PRECIO")
        for i in range(len(tablafinal)):
            tablafinal[i][x] = "$"+str(tablafinal[i][x])

        return render_template("clientabla.html", cliente=nombre, tabla=tablafinal, titulo=tablaorden, gasto=gasto)

@app.route('/prodbus')
def prodbus():
##### AGREGADO POR PEKE
    error = chequeoerror()
    if error:
        return render_template('error.html', error=error)
##### AGREGADO POR PEKE
    if 'username' not in session:
        return redirect(url_for('ingresar'))

    return render_template('prodbus.html')

@app.route('/productos', methods=["POST" , "GET"])
def productos():
##### AGREGADO POR PEKE
    error = chequeoerror()
    if error:
        return render_template('error.html', error=error)
##### AGREGADO POR PEKE
    if 'username' not in session:
        return redirect(url_for('index'))

    if request.method == "POST":
        filtro = request.form['nombreprod']
        if len(filtro) < 3:
            return render_template('prodbus.html', error=1)
        with open('ventas.csv','r') as archivo:
            tablacsv = csv.DictReader(archivo)
            listadoprod = []

            for linea in tablacsv:
                if filtro.lower() in linea["PRODUCTO"].lower():
                    listadoprod.append(linea["PRODUCTO"])

            listadoprod = list(set(listadoprod))

            if len(listadoprod) == 0:
                return render_template('prodbus.html', prod=listadoprod, lista=0)

            elif len(listadoprod) == 1:
                return redirect(url_for('prodtabla', filtro=listadoprod[0]))

            return render_template('prodbus.html', producto=listadoprod, lista=1)


@app.route('/prodtabla/<filtro>')
def prodtabla(filtro):
##### AGREGADO POR PEKE
    error = chequeoerror()
    if error:
        return render_template('error.html', error=error)
##### AGREGADO POR PEKE
    if 'username' not in session:
        return redirect(url_for('ingresar'))

    with open('ventas.csv','r') as archivo:
        tablacsv = csv.DictReader(archivo)

        cant = 0
        tabla = []
        tablafinal = []
        tablaorden = ["CODIGO","PRODUCTO","CLIENTE","PRECIO","CANTIDAD"]
        nombre = filtro.replace("%20", " ")

        for line in tablacsv:
            if line["PRODUCTO"] == nombre:
                tabla.append(line)

        for fila in range(len(tabla)):
            tablafinal.append([])
            for columna in range(len(tablaorden)):
                tablafinal[fila].append(tabla[fila][tablaorden[columna]])

        x = tablaorden.index("PRECIO")
        for i in range(len(tablafinal)):
            tablafinal[i][x] = "$"+str(tablafinal[i][x])

        for cantidad in range(len(tabla)):
            cant = cant + int(tabla[cantidad]["CANTIDAD"])

        return render_template("prodtabla.html", producto=nombre, cant=cant, tabla=tablafinal, titulo=tablaorden)

@app.route('/mejclie')
def mejclie():
##### AGREGADO POR PEKE
    error = chequeoerror()
    if error:
        return render_template('error.html', error=error)
##### AGREGADO POR PEKE
    if 'username' not in session:
        return redirect(url_for('ingresar'))

    with open('ventas.csv','r') as archivo:
        tablacsv = list(csv.DictReader(archivo))

        cant = 10
        tabla = []
        diccionario = {}

        for nombre in tablacsv:
            tabla.append(nombre["CLIENTE"])
        tabla = list(set(tabla))

        for gastado in range(len(tabla)):
            gasto = 0
            for linea in range(len(tablacsv)):
                if tablacsv[linea]["CLIENTE"] == tabla[gastado]:
                    gasto = gasto + (float(tablacsv[linea]["PRECIO"]) * int(tablacsv[linea]["CANTIDAD"]))
                diccionario[tabla[gastado]] = "$"+str(gasto)

        ordenado = sorted(diccionario.items(), key = lambda t:t[1], reverse=True)
        return render_template("mejclie.html", lista=ordenado[0:cant], cant=cant)

@app.route('/prodmas')
def prodmas():
##### AGREGADO POR PEKE
    error = chequeoerror()
    if error:
        return render_template('error.html', error=error)
##### AGREGADO POR PEKE
    if 'username' not in session:
        return redirect(url_for('ingresar'))
        
    with open('ventas.csv','r') as archivo:
        tablacsv = list(csv.DictReader(archivo))

        cant = 10
        tabla = []
        diccionario = {}

        for produc in tablacsv:
            tabla.append(produc["PRODUCTO"])
        tabla = list(set(tabla))

        for comprados in range(len(tabla)):
            compras = 0
            for line in range(len(tablacsv)):
                if tablacsv[line]["PRODUCTO"] == tabla[comprados]:
                    compras = compras + int(tablacsv[line]["CANTIDAD"])
            diccionario[tabla[comprados]] = compras

        ordenado = sorted(diccionario.items(), key = lambda t:t[1], reverse=True)
        return render_template("prodmas.html", lista=ordenado[0:cant], cant=cant)

if __name__ == "__main__":
    # app.run(host='0.0.0.0', debug=True)
    manager.run()
