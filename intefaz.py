# -*- coding: utf-8 -*-
"""
Created on Fri May 19 14:17:42 2023

@author: Eeduardo
"""

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import numpy as np
def antColonyOpti(nest, food):
    link = np.load('./link.npy')
    terreno_pos = np.load('./terreno.npy')
    
    pheromones= np.ones(len(link)) * 0.1  # Feromona
    pheromones=pheromones[:, np.newaxis]
    dist=np.zeros(len(link))
    vis_n=np.zeros(len(link))
    for i in range(len(link)):
        pnt1 = link[i, 0]
        pnt2 =link[i, 1]
        px1 = terreno_pos[pnt1-1, 0]
        px2 = terreno_pos[pnt2-1, 0]
        py1 = terreno_pos[pnt1-1, 1]
        py2 = terreno_pos[pnt2-1, 1]
        # Calculo de distancia
        dist[i]=np.sqrt((px1 - px2) ** 2 + (py1 - py2) ** 2)
        # factor de visibilidad
        vis_n[i]= 1 / dist[i]  
    vis_n=vis_n[:, np.newaxis]
    
    ## Calculo de probabilidad
    def select_next_link(current_link, available_links):
        if len(available_links) == 0:
            return None
        probabilities = np.zeros(len(available_links))
        total = 0
        for i, link in enumerate(available_links):
            pheromone = pheromones[link]
            probability = pheromone * vis_n[link]
            probabilities[i] = probability
            total += probability
        probabilities /= total
        next_link = np.random.choice(available_links, p=probabilities)
        return next_link
    
    Q = 10  # razon de apredizaje
    evaporation = 0.5 # porcentaje de vaporización de las feromonas en el terreno
    explorations =150# cantidad de exploraciones a realizar
    n_ants= 20# cantidad de hormigas exploradoras
    #nest = 21 # posición del nido en el terreno
    #food = 24# posición de la comida en el terreno
    # Variables para almacenar el recorrido de las hormigas
    ant_paths = np.zeros((n_ants, len(link)), dtype=int)
    ant_distances = np.zeros(n_ants)
    ant_distances = ant_distances[:, np.newaxis]
    visited_nodes = np.zeros((n_ants, 3), dtype=int)  # Almacenar los últimos 3 nodos visitados por cada hormiga
    
    # Algoritmo de optimización por colonia de hormigas
    way = []
    min_distance = np.inf
    
    for _ in range(explorations):
        
        for ant in range(n_ants):
            visited_links = [] 
            way = []
            last_link = 0
            ant_distances[ant] = 0
            ant_paths[ant, :] = 0
            distand =0
            current_link = nest
            way.append(current_link)
            while current_link != food:
                available_links = np.where(link[:, 0] == current_link)[0]
                test = np.array(visited_links)
                for i in range(len(visited_links)):
                    available_links = np.delete(available_links, np.where(available_links == test[i]))
                #available_links = np.delete(available_links, np.where(available_links == last_link))
    
                if len(available_links) > 0:
                    # Filtrar enlaces que conducen a nodos ya visitados en las últimas dos iteraciones
                    last_nodes = visited_nodes[ant][-3:]
                    available_links = [link for link in available_links if link not in last_nodes]
    
                    if len(available_links) > 0:
                        next_link_index = np.random.choice(len(available_links))
                        next_link = available_links[next_link_index]
                        visited_links.append(next_link)
                        ant_paths[ant, next_link] = 1
                        distand += dist[next_link]
                        ant_distances[ant] += dist[next_link]
                        #last_link = current_link
                        current_link = link[next_link, 1]
                        way.append(current_link)
    
                        # Actualizar la lista de nodos visitados
                        visited_nodes[ant] = np.roll(visited_nodes[ant], -1)
                        visited_nodes[ant][-1] = current_link
                    else:
                        break
                else:
                    break
    
                if distand > 15:
                    #print(f"Hormiga {ant + 1} descartada: recorrido demasiado largo")
                    break
    
            if distand <= 15 and way[-1] == food:
                if distand < min_distance:
                    best_rute = way
                    min_distance = distand
                # print(f"Hormiga {ant + 1} recorrido: {way}")
                # print(f"Costo de ruta de hormiga {ant + 1}: {ant_distances[ant]}")
                # Actualizacion feromonas
                pheromones *= (1 - evaporation)
                for link_index in np.where(ant_paths[ant] == 1)[0]:
                    pheromones[link_index] += Q / ant_distances[ant]
    
                
    # print(f"El mejor camino es  {best_rute}")
    # print(f"Costo de : {min_distance}")
    return best_rute, min_distance
                    

# Lista de estaciones de metro
estaciones = [
"Tacubaya",
"Centro Médico",
"Chabacano",
"Jamaica",
"Pantitlan",
"Oceanía",
"San Lázaro",
"Candelaria",
"Morelos",
"Pino Suárez",
"Salto del agua",
"Balderas",
"Tacuba",
"Hidalgo",
"Guerrero",
"Bellas Artes",
"Garibaldi",
"Consulado",
"La Raza",
"El Rosario",
"Intituto del Petroleo",
"Deportivo 18 de Marzo",
"Martin Carrera",
"Santa Anita",
"Mixcoac",
"Zapata",
"Ermita",
"Atlalilco"
]
def estacion2Num(esta1, esta2):
    nest = estaciones.index(esta1)+1
    food = estaciones.index(esta2)+1
    return nest,food

def way2string(way):
    cont= 1
    mensaje = ""
    for i in way:
        mensaje += f"{cont}. {estaciones[i-1]} \n"
        cont += 1
    return mensaje

def seleccionar_estacion():
    estacion_1 = combo_estacion_1.get()
    estacion_2 = combo_estacion_2.get()
    nest, food = estacion2Num(estacion_1, estacion_2)
    best, dist = antColonyOpti(nest, food)
    ruta = way2string(best)
    
    mensaje = f"Estación De Origen: {estacion_1}\nEstació De Destino: {estacion_2} \n" +ruta + f" \n \n \t Distancia Total: {round(dist*10, 2)} km"
    messagebox.showinfo("Ruta", mensaje)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Estaciones de Metro")
# Cargar la imagen
imagen = Image.open("metroFinal.jpg")
imagen = imagen.resize((500, 500), Image.BILINEAR  )
imagen = ImageTk.PhotoImage(imagen)

# Crear un widget de etiqueta para mostrar la imagen
label_imagen = ttk.Label(ventana, image=imagen)
label_imagen.pack()

# Etiqueta de la primera estación
label_estacion_1 = ttk.Label(ventana, text="Origen:")
label_estacion_1.pack()

# Menú desplegable para la primera estación
combo_estacion_1 = ttk.Combobox(ventana, values=estaciones)
combo_estacion_1.pack()

# Etiqueta de la segunda estación
label_estacion_2 = ttk.Label(ventana, text="Destino:")
label_estacion_2.pack()

# Menú desplegable para la segunda estación
combo_estacion_2 = ttk.Combobox(ventana, values=estaciones)
combo_estacion_2.pack()

# Botón para seleccionar las estaciones
boton_seleccionar = ttk.Button(ventana, text="Seleccionar", command=seleccionar_estacion)
boton_seleccionar.pack()

# Ejecutar la ventana principal
ventana.mainloop()