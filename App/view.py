"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """




import config as cf
import sys
import controller as ctr
from DISClib.ADT import list as lt
assert cf
import folium
import sys
from prettytable import PrettyTable as pt
import folium 
from collections import namedtuple
import numpy as np
import math
sys.setrecursionlimit(10000)

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar E instanciar el catálogo")
    print("2- REQ1")
    print("3- REQ2")
    print("4- REQ3")
    print("5- REQ4")
    print("6- REQ5")
    print("7- SALIR")
catalog = None

"""
Menu principal
"""

#Funciones getArrows y get_angle sacadas de https://instrovate.com/2019/07/01/tagging-two-locations-on-map-using-python-and-finding-distance-between-two-tagged-location-in-python/
def getArrows(locations, color='blue', size=8, n_arrows=3):
    
    '''
    Get a list of placed and rotated arrows or markers to be plotted
    
    Parameters
    locations : list of lists of latitude longitude that represent the begining and end of Line. 
                    this function Return list of arrows or the markers
    '''
    
    Point = namedtuple('Point', field_names=['lat', 'lon'])
    
    # creating point from Point named tuple
    point1 = Point(locations[0][0], locations[0][1])
    point2 = Point(locations[1][0], locations[1][1])
    
    # calculate the rotation required for the marker.  
    #Reducing 90 to account for the orientation of marker
    # Get the degree of rotation
    angle = get_angle(point1, point2) - 90
    
    # get the evenly space list of latitudes and longitudes for the required arrows

    arrow_latitude = np.linspace(point1.lat, point2.lat, n_arrows + 2)[1:n_arrows+1]
    arrow_longitude = np.linspace(point1.lon, point2.lon, n_arrows + 2)[1:n_arrows+1]
    
    final_arrows = []
    
    #creating each "arrow" and appending them to our arrows list
    for points in zip(arrow_latitude, arrow_longitude):
        final_arrows.append(folium.RegularPolygonMarker(location=points, 
                      fill_color=color, number_of_sides=3, 
                      radius=size, rotation=angle))
    return final_arrows

def get_angle(p1, p2):
    
    '''
    This function Returns angle value in degree from the location p1 to location p2
    
    Parameters it accepts : 
    p1 : namedtuple with lat lon
    p2 : namedtuple with lat lon
    
    This function Return the vlaue of degree in the data type float
    
    Pleae also refers to for better understanding : https://gist.github.com/jeromer/2005586
    '''
    
    longitude_diff = np.radians(p2.lon - p1.lon)
    
    latitude1 = np.radians(p1.lat)
    latitude2 = np.radians(p2.lat)
    
    x_vector = np.sin(longitude_diff) * np.cos(latitude2)
    y_vector = (np.cos(latitude1) * np.sin(latitude2) 
        - (np.sin(latitude1) * np.cos(latitude2) 
        * np.cos(longitude_diff)))
    angle = np.degrees(np.arctan2(x_vector, y_vector))
    
    # Checking and adjustring angle value on the scale of 360
    if angle < 0:
        return angle + 360
    return angle
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog=ctr.newCatalog()
        DataGrafoDir,DataGrafoNodir,CantCiudades,ciudad1,ciudad2=ctr.cargarDatos(catalog)
        b=pt()
        print("Airport Routes Digraph")
        print("Nodes:",DataGrafoDir["aero"])
        print("Edges:",DataGrafoDir["rutas"])
        print("First and last Airport")
        b.field_names = ["IATA", "Name", "City", "Country","Latitude","Longitude"]
        ari1=DataGrafoDir["inicialDIR"]
        ari2=DataGrafoDir["finalDIR"]
        b.add_row([ari1["IATA"],ari1["Name"],ari1["City"],ari1["Country"],ari1["Latitude"],ari1["Longitude"]])
        b.add_row([ari2["IATA"],ari2["Name"],ari2["City"],ari2["Country"],ari2["Latitude"],ari2["Longitude"]])
        print(b)
        C=pt()
        print("*"*20)
        print("Airport Routes Graph")
        print("Nodes:",DataGrafoNodir["aero"])
        print("Edges:",DataGrafoNodir["rutas"])
        print("First and last Airport")
        C.field_names = ["IATA", "Name", "City", "Country","Latitude","Longitude"]
        ari1=DataGrafoNodir["inicialNODIR"]
        ari2=DataGrafoNodir["finalNODIR"]
        C.add_row([ari1["IATA"],ari1["Name"],ari1["City"],ari1["Country"],ari1["Latitude"],ari1["Longitude"]])
        C.add_row([ari2["IATA"],ari2["Name"],ari2["City"],ari2["Country"],ari2["Latitude"],ari2["Longitude"]])
        print(C)
        print("*"*20)
        print("City Data")
        print("Number of cities are:",CantCiudades)
        print("First and last city:")
        C=pt()
        C.field_names=["city","country","lat","lng","population"]
        C.add_row([ciudad1["city"],ciudad1["country"],ciudad1["lat"],ciudad1["lng"],ciudad1["population"]])
        C.add_row([ciudad2["city"],ciudad2["country"],ciudad2["lat"],ciudad2["lng"],ciudad2["population"]])
        print(C)
    elif int(inputs[0]) == 2:
        ordenada=ctr.req1(catalog)
        cantidad=int(input("Elija cuántos quiere ver en pantalla:"))
        p=pt()
        p.field_names=["Name","City","Country","IATA","Connections","inbound","outbound"]
        i=0
        lista_vertices=lt.newList("ARRAY_LIST",ctr.compara)
        for elemento in lt.iterator(ordenada):
            lt.addLast(lista_vertices,elemento["aero"]["IATA"])
        for elemento in lt.iterator(ordenada):
            if(i==cantidad):
                break
            p.add_row([elemento["aero"]["Name"],elemento["aero"]["City"],elemento["aero"]["Country"],elemento["aero"]["IATA"],elemento["suma"],elemento["entran"],elemento["salen"]])
            i+=1
        print(p)
        #BONO 7
        m = folium.Map(location=[-40.81330109,172.7749939], zoom_start=4)
        número=0
        arcos=ctr.obtenerArcos(catalog["dirigido"])
        for i in lt.iterator(arcos):
            result1,result2=lt.isPresent(lista_vertices,i["vertexA"]),lt.isPresent(lista_vertices,i["vertexB"])
            if(result1!=0 and result2!=0):
                e2=lt.getElement(ordenada,result2)
                e=lt.getElement(ordenada,result1)
                inicio = [float(e["aero"]["Latitude"]),float(e["aero"]["Longitude"])]
                llegada=[float(e2["aero"]["Latitude"]),float(e2["aero"]["Longitude"])]
                
                toltip1=e["aero"]["City"]+":"+str(result1)
                toltip2=e2["aero"]["City"]+":"+str(result2)
                
                folium.Marker(inicio, popup="<i>"+e["aero"]["IATA"]+"</i>", tooltip=toltip1).add_to(m)
                folium.Marker(llegada, popup="<i>"+e2["aero"]["IATA"]+"</i>", tooltip=toltip2).add_to(m)

                folium.PolyLine(locations=[inicio, llegada], color='red').add_to(m)
                arrows = getArrows(locations=[inicio, llegada], n_arrows=15)
                for arrow in arrows:
                    arrow.add_to(m)
        m.save('REQ1.HTML')
    elif int(inputs[0]) == 3:
        IATA1=input("Elija su aeropuerto número 1:")
        IATA2=input("Elija su aeropuerto número 2:")
        númeroComponentes,conectados,search=ctr.req2(catalog,IATA1,IATA2)
        print("Hay una cantidad de:",númeroComponentes,"componentes fuertemente conectados.")
        print("¿",IATA1,"y",IATA2,"están fuertemente conectados?=",conectados)
        #BONO 7
        if(conectados):
            m = folium.Map(location=[-40.81330109,172.7749939], zoom_start=4)
            arcos=ctr.componenteConectados(search,IATA1,IATA2,catalog["dirigido"])
            for i in lt.iterator(arcos):
                e=ctr.buscar_aero(catalog,i["vertexA"])
                e2=ctr.buscar_aero(catalog,i["vertexB"])
                inicio = [float(e["Latitude"]),float(e["Longitude"])]
                llegada=[float(e2["Latitude"]),float(e2["Longitude"])]
                toltip1=e["City"]
                toltip2=e2["City"]
                folium.Marker(inicio, popup="<i>"+e["IATA"]+"</i>", tooltip=toltip1).add_to(m)
                folium.Marker(llegada, popup="<i>"+e2["IATA"]+"</i>", tooltip=toltip2).add_to(m)
                folium.PolyLine(locations=[inicio, llegada], color='red').add_to(m)
                arrows = getArrows(locations=[inicio, llegada], n_arrows=15)
                for arrow in arrows:
                    arrow.add_to(m)
                m.save("REQ2.HTML")
    elif int(inputs[0])== 4:
        ciudad1=input("Digite la ciudad de origen:")
        ciudad2=input("Digite la ciudad de destino:")
        ciudades_disponibles_origen=ctr.encontrarOpciones(catalog,ciudad1)
        ciudades_disponibles_destino=ctr.encontrarOpciones(catalog,ciudad2)
        print("Opciones para su ciudad:",ciudad1)
        p=pt()
        p.field_names=["NúmeroElección","city","lat","lng","country","iso2","iso3","admin_name","capital"]
        for i in range(1,lt.size(ciudades_disponibles_origen)+1):
            elemento=lt.getElement(ciudades_disponibles_origen,i)
            p.add_row([str(i),elemento["city"],elemento["lat"],elemento["lng"],elemento["country"],elemento["iso2"],elemento["iso3"],elemento["admin_name"],elemento["capital"]])
        print(p)        
        elección1=int(input("Digite el 'NúmeroElección' para la ciudad de origen: "))
        print("*"*10)
        print("Opciones para su ciudad:",ciudad2)
        p=pt()
        p.field_names=["NúmeroElección","city","lat","lng","country","iso2","iso3","admin_name","capital"]
        for i in range(1,lt.size(ciudades_disponibles_destino)+1):
            elemento=lt.getElement(ciudades_disponibles_destino,i)
            p.add_row([str(i),elemento["city"],elemento["lat"],elemento["lng"],elemento["country"],elemento["iso2"],elemento["iso3"],elemento["admin_name"],elemento["capital"]])
        print(p)
        elección2=int(input("Digite el 'NúmeroElección' para la ciudad de origen: "))

        ciudad1=lt.getElement(ciudades_disponibles_origen,elección1)
        ciudad2=lt.getElement(ciudades_disponibles_destino,elección2)
        aero1,valorc1,aero2,valorc2=ctr.buscarAeroCercano(catalog,ciudad1,ciudad2)
        print("El punto de partida es:")
        p=pt()
        p.field_names=["IATA","Name","City","Country"]
        p.add_row([aero1["IATA"],aero1["Name"],aero1["City"],aero1["Country"]])
        print(p)
        print("*"*100)
        print("El punto de llegada es:")
        p=pt()
        p.field_names=["IATA","Name","City","Country"]
        p.add_row([aero2["IATA"],aero2["Name"],aero2["City"],aero2["Country"]])
        print(p)
        Ruta,costoTotal=ctr.rutamínima(catalog,aero1,aero2,valorc1,valorc2)
        print("Distancia total:",costoTotal)
        print("Ruta:")
        p=pt()
        p.field_names=["Airline","Departure","Destination","distance_km"]
        p.add_row(["",ciudad1["city"],aero1["IATA"],valorc1])
        for i in lt.iterator(Ruta):
            p.add_row([i["Airline"],i["vertexA"],i["vertexB"],i["weight"]])
        p.add_row(["",aero2["IATA"],ciudad2["city"],valorc2])
        print(p)
        #BONO 7
        m = folium.Map(location=[-40.81330109,172.7749939], zoom_start=4)
        número=0
        for i in lt.iterator(Ruta):
            e=ctr.buscar_aero(catalog,i["vertexA"])
            e2=ctr.buscar_aero(catalog,i["vertexB"])
            inicio = [float(e["Latitude"]),float(e["Longitude"])]
            llegada=[float(e2["Latitude"]),float(e2["Longitude"])]
            toltip1=e["City"]
            toltip2=e2["City"]
            folium.Marker(inicio, popup="<i>"+e["IATA"]+"</i>", tooltip=toltip1).add_to(m)
            folium.Marker(llegada, popup="<i>"+e2["IATA"]+"</i>", tooltip=toltip2).add_to(m)
            folium.PolyLine(locations=[inicio, llegada], color='red').add_to(m)
            arrows = getArrows(locations=[inicio, llegada], n_arrows=15)
            for arrow in arrows:
                arrow.add_to(m)
        m.save("REQ3.HTML")
    elif int(inputs[0])==5:
        ciudad_origen=input("Digite la ciudad de origen:")
        cantidad_millas=float(input("Digite la cantidad de millas:"))
        ciudades_disponibles_origen=ctr.encontrarOpciones(catalog,ciudad_origen)
        print("Opciones para su ciudad:",ciudad_origen)
        p=pt()
        p.field_names=["NúmeroElección","city","lat","lng","country","iso2","iso3","admin_name","capital"]
        for i in range(1,lt.size(ciudades_disponibles_origen)+1):
            elemento=lt.getElement(ciudades_disponibles_origen,i)
            p.add_row([str(i),elemento["city"],elemento["lat"],elemento["lng"],elemento["country"],elemento["iso2"],elemento["iso3"],elemento["admin_name"],elemento["capital"]])
        print(p)        
        elección1=int(input("Digite el 'NúmeroElección' para la ciudad de origen: "))
        ciudad1=lt.getElement(ciudades_disponibles_origen,elección1)
        aero1=ctr.buscarAeroCercano1(catalog,ciudad1)
        msg,arcos_MST_desdeVERTEX,peso_total_MSTreal,VERTICES=ctr.REQ4(catalog,aero1["IATA"],cantidad_millas)
        print("Número de nodos conectados:",VERTICES)
        print("Costo total del MST:",peso_total_MSTreal,"kilometros")
        print("Aeropuerto de partida")
        p=pt()
        p.field_names=["Name","City","Country","IATA"]
        p.add_row([aero1["Name"],aero1["City"],aero1["Country"],aero1["IATA"]])
        print(p)
        print("RUTA")
        p=pt()
        Rutax=arcos_MST_desdeVERTEX
        p.field_names=["Departure","Destination","distance_km"]
        for i in lt.iterator(Rutax):
            p.add_row([i["vertexA"],i["vertexB"],i["weight"]])
        print(p)
        print(msg)
        
        #BONO 7
        m = folium.Map(location=[-40.81330109,172.7749939], zoom_start=4)
        número=0
        for i in lt.iterator(arcos_MST_desdeVERTEX):
            e=ctr.buscar_aero(catalog,i["vertexA"])
            e2=ctr.buscar_aero(catalog,i["vertexB"])
            inicio = [float(e["Latitude"]),float(e["Longitude"])]
            llegada=[float(e2["Latitude"]),float(e2["Longitude"])]
            toltip1=e["City"]
            toltip2=e2["City"]
            if(e["IATA"]==aero1["IATA"]):
                folium.Marker(inicio, popup="<i>"+e["IATA"]+"</i>", tooltip=toltip1,icon=folium.Icon(color="blue", icon="info-sign")).add_to(m)
            else:
                folium.Marker(inicio, popup="<i>"+e["IATA"]+"</i>", tooltip=toltip1).add_to(m)
            if(e2["IATA"]==aero1["IATA"]):
                folium.Marker(llegada, popup="<i>"+e2["IATA"]+"</i>", tooltip=toltip2,icon=folium.Icon(color="blue", icon="info-sign")).add_to(m)
            else:
                folium.Marker(llegada, popup="<i>"+e2["IATA"]+"</i>", tooltip=toltip2).add_to(m)
            folium.PolyLine(locations=[inicio, llegada], color='red').add_to(m)
            arrows = getArrows(locations=[inicio, llegada], n_arrows=15)
            for arrow in arrows:
                arrow.add_to(m)
        m.save("REQ4.HTML")
    elif int(inputs[0])==6:
        Sal=input("Digite el aeropuerto que sale de funcionamiento:")
        resultado=ctr.req5(catalog,Sal)
        p=pt()
        p.field_names=["IATA","Name","City","Country"]
        print("Estos aeropuertos podrían verse afectados si",Sal,"sale de funcionamiento.")
        for aero1 in lt.iterator(resultado):
            p.add_row([aero1["IATA"],aero1["Name"],aero1["City"],aero1["Country"]])
        print(p)
        #BONO 7
        m = folium.Map(location=[-40.81330109,172.7749939], zoom_start=4)
        for i in lt.iterator(ctr.obtenerArcos(catalog["dirigido"])):
            e=ctr.buscar_aero(catalog,i["vertexA"])
            e2=ctr.buscar_aero(catalog,i["vertexB"])
            inicio = [float(e["Latitude"]),float(e["Longitude"])]
            llegada=[float(e2["Latitude"]),float(e2["Longitude"])]
            toltip1=e["City"]
            toltip2=e2["City"]
            cond1=e["IATA"]==Sal
            cond2=e2["IATA"]==Sal
            if(cond1):
                folium.Marker(inicio, popup="<i>"+e["IATA"]+"</i>", tooltip=toltip1,icon=folium.Icon(color="red", icon="info-sign")).add_to(m)
            else:
                folium.Marker(inicio, popup="<i>"+e["IATA"]+"</i>", tooltip=toltip1).add_to(m)
                
            if(cond2):
                folium.Marker(llegada, popup="<i>"+e2["IATA"]+"</i>", tooltip=toltip2,icon=folium.Icon(color="red", icon="info-sign")).add_to(m)
            else:
                folium.Marker(inicio, popup="<i>"+e["IATA"]+"</i>", tooltip=toltip1).add_to(m)
            
            if(cond2 or cond1):
                folium.PolyLine(locations=[inicio, llegada], color='red').add_to(m)
            else:
                folium.PolyLine(locations=[inicio, llegada], color='blue').add_to(m)
            if(cond2 or cond1):
                folium.PolyLine(locations=[inicio, llegada], color='red').add_to(m)
                arrows = getArrows(locations=[inicio, llegada], n_arrows=15,color="red")
            else:
                folium.PolyLine(locations=[inicio, llegada], color='blue').add_to(m)
                arrows = getArrows(locations=[inicio, llegada], n_arrows=15,color="blue")
            for arrow in arrows:
                arrow.add_to(m)
        m.save("REQ5.HTML")
    elif int(inputs[0])==7:
        sys.exit(0)
sys.exit(0)

