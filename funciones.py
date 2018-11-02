import csv

def chequeoerror():
    ##### AGREADO POR PEKE
    try:
        with open('ventas.csv','r') as archivo:
            tablacsv = list(csv.DictReader(archivo))
            tablaorden = ["CODIGO","PRODUCTO","CLIENTE","PRECIO","CANTIDAD"]
            lista = []
            for i in tablacsv:
                for a in tablaorden:
                    if i[a] == "" or str(i[a]).isspace():
                        lista.append(f"Al registro numero {tablacsv.index(i)} le falta el campo {a}.")

            for i in range(len(tablacsv)):
                if tablacsv[i]["CODIGO"][0:3].isalpha() and tablacsv[i]["CODIGO"][3:6].isnumeric() and len(tablacsv[i]["CODIGO"]) == 6:
                    continue
                else:
                   lista.append(f"El Codigo del registro numero {i} tiene un formato invalido.")

            for i in range(len(tablacsv)):
                if float(tablacsv[i]["CANTIDAD"]) % 1 != 0:
                    lista.append(f"El campo CANTIDAD del registro numero {i} no es un numero entero.")

                if float(tablacsv[i]["PRECIO"]):
                    continue
                else:
                    lista.append(f"El campo PRECIO del registro numero {i} no es un numero decimal.")

            return lista

    except FileNotFoundError:
        return "Archivo no encontrado."


def ultventfun():
    with open('ventas.csv','r') as archivo:
        tablacsv = csv.DictReader(archivo)
        tablaorden = ["CODIGO","PRODUCTO","CLIENTE","PRECIO","CANTIDAD"]
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

        return (tablafinal,tablaorden)

def filtrar(campo, filtro):
    with open('ventas.csv','r') as archivo:
        tablacsv = csv.DictReader(archivo)
        listado = []

        for linea in tablacsv:
            if filtro.lower() in linea[campo].lower():
                listado.append(linea[campo])

        listado = list(set(listado))

        return listado

def mostrar(campo, filtro):
    with open('ventas.csv','r') as archivo:
        tablacsv = csv.DictReader(archivo)

        cant = 0
        tabla = []
        tablafinal = []
        tablaorden = ["CODIGO","PRODUCTO","CLIENTE","PRECIO","CANTIDAD"]
        nombre = filtro.replace("%20", " ")

        for line in tablacsv:
            if line[campo] == nombre:
                tabla.append(line)

        for fila in range(len(tabla)):
            tablafinal.append([])
            for columna in range(len(tablaorden)):
                tablafinal[fila].append(tabla[fila][tablaorden[columna]])

        x = tablaorden.index("PRECIO")
        for i in range(len(tablafinal)):
            tablafinal[i][x] = "$"+str(tablafinal[i][x])

        if campo == "PRODUCTO":
            for cantidad in range(len(tabla)):
                cant = cant + int(tabla[cantidad]["CANTIDAD"])
        elif campo == "CLIENTE":
            for precio in range(len(tabla)):
                cant = cant + (int(tabla[precio]["PRECIO"])*int(tabla[precio]["CANTIDAD"]))

        return tablafinal, tablaorden, cant, nombre

def mejores(campo):
    with open('ventas.csv','r') as archivo:
        tablacsv = list(csv.DictReader(archivo))

        cant = 10
        tabla = []
        diccionario = {}

        for nombre in tablacsv:
            tabla.append(nombre[campo])
        tabla = list(set(tabla))

        for compra in range(len(tabla)):
            valor = 0
            for linea in range(len(tablacsv)):
                if tablacsv[linea][campo] == tabla[compra]:
                    if campo == "CLIENTE":
                        valor = valor + (float(tablacsv[linea]["PRECIO"]) * int(tablacsv[linea]["CANTIDAD"]))
                    elif campo == "PRODUCTO":
                        valor = valor + int(tablacsv[linea]["CANTIDAD"])
            diccionario[tabla[compra]] = ("$"+str(valor) if campo == "CLIENTE" else valor)
        
        ordenado = sorted(diccionario.items(), key = lambda t:t[1], reverse=True)
        return ordenado

##### AGREADO POR PEKE