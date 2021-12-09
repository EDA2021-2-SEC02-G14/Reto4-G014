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
 """

import config as cf
import model as md
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de librosasd
def newCatalog():
    return md.newCatalog()
# Funciones para la carga de datos
def cargarDatos(catalog):
    #CantCiudad={total:0,primer:{},ult:{}}
    #CantRGrafoDIR={rutas:0,aero:0,primer:{},último:{}}
    CantRGrafoDIR,CantRGrafoNODIR=cargar_aeropuertos(catalog)
    CantCiudades,ciudad1,ciudad2=cargar_ciudades(catalog)
    cargar_rutas(catalog)
    CantRGrafoDIR["rutas"]=md.CantEdges(catalog["dirigido"])
    CantRGrafoNODIR["rutas"]=md.CantEdges(catalog["no_dirigido"])
    CantRGrafoDIR["aero"]=md.CantVertex(catalog["dirigido"])
    CantRGrafoNODIR["aero"]=md.CantVertex(catalog["no_dirigido"])
    return CantRGrafoDIR,CantRGrafoNODIR,CantCiudades,ciudad1,ciudad2
    
def cargar_aeropuertos(catalog):
    archivo=cf.data_dir+"airports-utf8-small.csv"
    lista_aeropuertos=csv.DictReader(open(archivo,encoding="utf-8"))
    contador=0
    inicial=""
    for aeropuerto in lista_aeropuertos:
        if(contador == 0):
            inicial=aeropuerto
            contador+=1
        md.agregaraero(catalog,aeropuerto)
        
    final=aeropuerto
    return {"inicialDIR":inicial,"finalDIR":final},{"inicialNODIR":inicial,"finalNODIR":final}
    
def cargar_rutas(catalog):
    archivo=cf.data_dir+"routes-utf8-small.csv"
    lista_rutas=csv.DictReader(open(archivo,encoding="utf-8"))
    for ruta in lista_rutas:
        md.agregarruta(catalog,ruta)
    

def cargar_ciudades(catalog):
    archivo=cf.data_dir+"worldcities-utf8.csv"
    lista_ciudades=csv.DictReader(open(archivo,encoding="utf-8"))
    primerax=None
    for ciudad in lista_ciudades:
        primera=md.AgregarCiudades(catalog,ciudad)
        if(primera != None):
            primerax=primera
    ultima=ciudad
    return md.cantidadCiudades(catalog["ciudades"]),primerax,ultima
# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def req1(catalogo):
    return md.req1(catalogo)
def req2(catalogo,IATA1,IATA2):
    return md.req2(catalogo,IATA1,IATA2)
def encontrarOpciones(catalog,ciudad):
    return md.encontrarOpciones(catalog,ciudad)
def buscarAeroCercano(catalog,ciudad1,ciudad2):
    return md.encontrarAeroCercano(catalog,ciudad1,ciudad2)
def buscarAeroCercano1(catalog,ciudad1):
    return md.encontrarAeroCercano1(catalog,ciudad1)
def req5(catalog,Sal):
    return md.req5(catalog,Sal)
def rutamínima(catalog,aero1,aero2,valorc1,valorc2):
    return md.rutamínima(catalog,aero1,aero2,valorc1,valorc2)
def REQ4(catalog,aero,cantidad_millas):
    return md.REQ4(catalog,aero,cantidad_millas)
def obtenerArcos(graph):
    return md.obtenerArcos(graph)
def compara(el1,el2):
    return md.comparaLista(el1,el2)
def componenteConectados(search,ver1,ver2,grafo):
    return md.componenteConectados(search,ver1,ver2,grafo)
def buscar_aero(catalog,iata):
    return md.buscar_aero(catalog,iata)





