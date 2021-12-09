"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from DISClib.Algorithms.Graphs import dfs
from DISClib.DataStructures.adjlist import newGraph
import config as cf
import csv
from DISClib.DataStructures import edge as e
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import graph as gr
from DISClib.Algorithms.Sorting import mergesort as mgs
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import prim as pr
from DISClib.ADT import stack as stk
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog():
    model={"dirigido":gr.newGraph(directed=True,comparefunction=comparador_Grafo,size=181),
            "no_dirigido":gr.newGraph(directed=False,comparefunction= comparador_Grafo,size=181),
            "ciudades":mp.newMap(numelements=41001,maptype="PROBING",comparefunction=comparador_Grafo),
            "aeropuertos":mp.newMap(numelements=41001,maptype="PROBING",comparefunction=comparador_Grafo),
            "AeroLista":lt.newList("ARRAY_LIST"),"ciudades_lista":lt.newList("ARRAY_LIST")}
    return model
# Funciones para agregar informacion al 
def agregaraero(catalog,aero):
    if not mp.contains(catalog["aeropuertos"],aero["IATA"]):
        mp.put(catalog["aeropuertos"],aero["IATA"],aero)
        gr.insertVertex(catalog["dirigido"],aero["IATA"])
        gr.insertVertex(catalog["no_dirigido"],aero["IATA"])
        lt.addLast(catalog["AeroLista"],aero)
def cantidadCiudades(map):
    valores=mp.valueSet(map)
    contador=0
    for i in lt.iterator(valores):
        contador+=lt.size(i)
    return contador


def agregarruta(catalog,ruta):
    """
    Guarda los dos grafos tanto dirigidos como no dirigidos
    los dirigidos los guarda de una vez
    para los no dirigidos, se sabe que se acaba de agregar un camino, entonces hay que buscar uno de vuelta,
    si el de vuelta existe agrega la conexión en el no dirigido.
    """
    graphDir=catalog["dirigido"]
    graphNODIR=catalog["no_dirigido"]
    peso=float(ruta["distance_km"])
    C=ruta["Departure"]
    D=ruta["Destination"]
    gr.addEdge(graphDir,C,D,peso)
    gr.getEdge(graphDir,C,D)["Airline"]=ruta["Airline"]
    vuelta=gr.getEdge(graphDir,D,C)
    if(vuelta!= None and gr.getEdge(graphNODIR,C,D)==None):
        A=vuelta["vertexA"]
        B=vuelta["vertexB"]
        gr.addEdge(graphNODIR,A,B,e.weight(vuelta))
        gr.getEdge(graphNODIR,A,B)["Airline"]=ruta["Airline"]
    

def AgregarCiudades(catalog,ciudad):
    ciudades=catalog["ciudades"]
    if not mp.contains(ciudades,ciudad["city"]):
        mismo_nombre=lt.newList("ARRAY_LIST")
        lt.addLast(mismo_nombre,ciudad)
        mp.put(ciudades,ciudad["city"],mismo_nombre)
    else:
        mismo_nombre=me.getValue(mp.get(ciudades,ciudad["city"]))
        lt.addLast(mismo_nombre,ciudad)
    lt.addLast(catalog["ciudades_lista"],ciudad)
    if(mp.size(ciudades)==1):
        return ciudad

# Funciones para creacion de datos

# Funciones de consulta
def buscarAero(catalog,aero):
    aeropuertos=catalog["aeropuertos"]
    return me.getValue(mp.get(aeropuertos,aero))
def req1(catalogo):
    grafo=catalogo["dirigido"]
    vertices=gr.vertices(grafo)
    lista_vertices=lt.newList("ARRAY_LIST",comparaAeroSTRUCT)
    for i in lt.iterator(vertices):
        salen=gr.outdegree(grafo,i)
        entran=gr.indegree(grafo,i)
        struct={"aero":buscarAero(catalogo,i),"entran":entran,"salen":salen,"suma":entran+salen}
        lt.addLast(lista_vertices,struct)
    ordenada=mgs.sort(lista_vertices,comparador_vertices)
    return ordenada
def req2(catalogo,IATA1,IATA2):
    kosaraju=scc.KosarajuSCC(catalogo["dirigido"])
    same_component=scc.stronglyConnected(kosaraju,IATA1,IATA2)
    return scc.connectedComponents(kosaraju),same_component,kosaraju
def ciudadMásCercana(catalogo,aero):
    lataero1=float(aero["Latitude"])
    longaero1=float(aero["Longitude"])
    Ciudades=catalogo["ciudades_lista"]
    mas_pequeñoC1=""
    valorC1=-1
    for City in lt.iterator(Ciudades):
        LatC=float(City["lat"])
        LonC=float(City["lng"]) 
        if(valorC1 == -1):
            mas_pequeñoC1=City
            valorC1=haversine(LonC,LatC,longaero1, lataero1)
        else:
            distanciaC1AERO=haversine(LonC,LatC,longaero1, lataero1)
            if distanciaC1AERO<=valorC1:
                valorC1=distanciaC1AERO
                mas_pequeñoC1=City
    return mas_pequeñoC1
def obtenerArcos(graph):
    return gr.edges(graph)
def encontrarOpciones(catalog,ciudad):
    ciudades=catalog["ciudades"]
    return me.getValue(mp.get(ciudades,ciudad))
def encontrarAeroCercano1(catalog,ciudad1):
    latCiudad1=float(ciudad1["lat"])
    longCiudad1=float(ciudad1["lng"])
    mas_pequeñoC1=""
    Aeropuertos=catalog["AeroLista"]
    valorC1=-1
    for AERO in lt.iterator(Aeropuertos):
        LatC=float(AERO["Latitude"])
        LonC=float(AERO["Longitude"]) 
        if(valorC1 == -1):
            mas_pequeñoC1=AERO
            valorC1=haversine(LonC,LatC,longCiudad1,latCiudad1)
        else:
            distanciaC1AERO=haversine(LonC,LatC,longCiudad1,latCiudad1)
            if distanciaC1AERO<=valorC1:
                valorC1=distanciaC1AERO
                mas_pequeñoC1=AERO
    return mas_pequeñoC1
def encontrarAeroCercano(catalog,ciudad1,ciudad2):
    latCiudad1=float(ciudad1["lat"])
    longCiudad1=float(ciudad1["lng"])

    latCiudad2=float(ciudad2["lat"])
    longCiudad2=float(ciudad2["lng"])
    Aeropuertos=catalog["AeroLista"]
    mas_pequeñoC1=""
    valorC1=-1
    mas_pequeñoC2=""
    valorC2=-1

    for AERO in lt.iterator(Aeropuertos):
        LatC=float(AERO["Latitude"])
        LonC=float(AERO["Longitude"]) 
        if(valorC1 == -1):
            mas_pequeñoC1=AERO
            valorC1=haversine(LonC,LatC,longCiudad1,latCiudad1)
        else:
            distanciaC1AERO=haversine(LonC,LatC,longCiudad1,latCiudad1)
            if distanciaC1AERO<=valorC1:
                valorC1=distanciaC1AERO
                mas_pequeñoC1=AERO

    for AERO in lt.iterator(Aeropuertos):
        LatC=float(AERO["Latitude"])
        LonC=float(AERO["Longitude"]) 
        if(valorC2 == -1):
            mas_pequeñoC2=AERO
            valorC2=haversine(LonC,LatC,longCiudad2,latCiudad2)
        else:
            distanciaC2AERO=haversine(LonC,LatC,longCiudad2,latCiudad2)
            if distanciaC2AERO<=valorC2:
                valorC2=distanciaC2AERO
                mas_pequeñoC2=AERO
    return mas_pequeñoC1,valorC1,mas_pequeñoC2,valorC2
def rutamínima(catalog,aero1,aero2,ciudad_aero1,ciudad_aero2):
    Dijkstra=djk.Dijkstra(catalog["dirigido"],aero1["IATA"])
    stack=djk.pathTo(Dijkstra,aero2["IATA"])
    camino=lt.newList("ARRAY_LIST")
    while stk.size(stack)>0:
        lt.addLast(camino,stk.pop(stack))
    Distancia=djk.distTo(Dijkstra,aero2["IATA"])+ciudad_aero1+ciudad_aero2#Distancia contando dezplazamiento desde las ciudades hasta los aeropuertos
    return camino,Distancia


def buscar_aero(catalog,iata):
    return me.getValue(mp.get(catalog["aeropuertos"],iata))
        

# Funciones utilizadas para comparar elementos dentro de una lista
def comparador_Grafo(elemento1,elemento2):
    llave2=me.getKey(elemento2)
    if (elemento1 == llave2):
        return 0
    elif elemento1 > llave2:
        return 1
    else:
        return -1

def comparador_vertices(el1,el2):
    return el1["suma"]>=el2["suma"]
        

def CantVertex(graph):
    return gr.numVertices(graph)
def CantEdges(graph):
    return gr.numEdges(graph)
def hacerMST(catalog):
    Search=pr.PrimMST(catalog["no_dirigido"])
    lista=pr.edgesMST(catalog["no_dirigido"],Search)
    grafoMST=lista["mst"]
    ARCOS=lt.newList("ARRAY_LIST")
    MST_graph=gr.newGraph(directed=False,comparefunction=comparador_Grafo)
    for i in lt.iterator(grafoMST):
        if not gr.containsVertex(MST_graph,i["vertexA"]):
            gr.insertVertex(MST_graph,i["vertexA"])
        if not gr.containsVertex(MST_graph,i["vertexB"]):
            gr.insertVertex(MST_graph,i["vertexB"])
        gr.addEdge(MST_graph,i["vertexA"],i["vertexB"],i["weight"])
        lt.addLast(ARCOS,i)
    return MST_graph
def REQ4(catalog,partida,millas):
    GRAFO=hacerMST(catalog)
    Kilometros=1.60*millas
    arcos_MST_desdeVERTEX,peso_total_MSTreal=DepthFirstSearch(GRAFO,partida)
    msg=""
    peso_total_MSTreal=peso_total_MSTreal
    if(peso_total_MSTreal*2>=Kilometros):
        SS=peso_total_MSTreal*2-Kilometros
        msg="Faltó una cantidad de "+str(SS/1.60)+" millas para completar el viaje"
    else:
        SS=Kilometros-peso_total_MSTreal*2
        msg="Sobró una cantidad de "+str(SS/1.60)+" millas para completar el viaje"
    return msg,arcos_MST_desdeVERTEX,peso_total_MSTreal,gr.numVertices(GRAFO)

def req5(catalog,Sal):
    grafo=catalog["dirigido"]
    afectados=lt.newList("ARRAY_LIST",comparaDICT)
    for i in lt.iterator(gr.edges(grafo)):
        if(i["vertexA"]==Sal):
            aero1=me.getValue(mp.get(catalog["aeropuertos"],i["vertexB"]))
            if(lt.isPresent(afectados,aero1)==0):
                lt.addLast(afectados,aero1)
        elif(i["vertexB"]==Sal):
            aero1=me.getValue(mp.get(catalog["aeropuertos"],i["vertexA"]))
            if(lt.isPresent(afectados,aero1)==0):
                lt.addLast(afectados,aero1)
    return afectados


#DFS MODIFICADO, se encarga de contar los vértices e ir sumando a medida que cambia de vértice para establecer la cantidad de vértices que puede visitar el usuario.
def DepthFirstSearch(graph, source):
    """
    Genera un recorrido DFS sobre el grafo graph
    Args:
        graph:  El grafo a recorrer
        source: Vertice de inicio del recorrido.
    Returns:
        Una estructura para determinar los vertices
        conectados a source
    Raises:
        Exception
    """
    
    search = {'source': source,
              'visited': None}
    search['visited'] = mp.newMap(numelements=gr.numVertices(graph),
                                       maptype='PROBING',
                                       comparefunction=graph['comparefunction']
                                       )
    mp.put(search['visited'], source, {'marked': True, 'edgeTo': None})
    limite={"PESO MST":0,"ARCOS":lt.newList("ARRAY_LIST",cmpfunction=comparaLista)}
    dfsVertex(search, graph, source,limite)
    return limite["ARCOS"],limite["PESO MST"]
def dfsVertex(search, graph, vertex,limite):
    adjlst = gr.adjacents(graph, vertex)
    for w in lt.iterator(adjlst):
        visited = mp.get(search['visited'], w)
        if visited is None:
            mp.put(search['visited'],
                    w, {'marked': True, 'edgeTo': vertex})
            arco=gr.getEdge(graph,vertex,w)
            lt.addLast(limite["ARCOS"],arco)
            limite["PESO MST"]+=arco["weight"]
            dfsVertex(search, graph, w,limite)
def compare_Vertex(ver1,ver2):
    return ver1[1]<=ver2[1]
def comparaLista(el1,el2):
    if (el1 == el2):
        return 0
    elif el1 > el2:
        return 1
    else:
        return -1
def comparaDICT(el1,el2):
    if (el1["id"] == el2["id"]):
        return 0
    elif el1["id"] > el2["id"]:
        return 1
    else:
        return -1


def comparaAeroSTRUCT(el1,el2):
    if (el1["aero"] == el2["aero"]):
        return 0
    elif el1["aero"] > el2["aero"]:
        return 1
    else:
        return -1
def componenteConectados(search,ver1,ver2,grafo):
    search1=scc.sccCount(grafo,search,ver1)
    search2=scc.sccCount(grafo,search,ver2)
    cl=me.getValue(mp.get(search1["idscc"],ver1))
    cl2=me.getValue(mp.get(search2["idscc"],ver2))
    vertices_de_la_componente=lt.newList("ARRAY_LIST",comparaLista)
    if(cl == cl2):
        for i in lt.iterator(gr.vertices(grafo)):
            searchc=scc.sccCount(grafo,search,i)
            componente=me.getValue(mp.get(searchc["idscc"],i))
            if(componente== cl):
                lt.addLast(vertices_de_la_componente,i)
    arcos=gr.edges(grafo)
    componente=lt.newList("ARRAY_LIST")
    for i in lt.iterator(arcos):
        if(lt.isPresent(vertices_de_la_componente,i["vertexA"])!=0 and lt.isPresent(vertices_de_la_componente,i["vertexB"])!=0):
            lt.addLast(componente,i)
    return componente



# Funciones de ordenamiento
from math import radians, cos, sin, asin, sqrt
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r