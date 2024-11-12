import heapq

# Función para encontrar la ruta más corta usando Dijkstra
def encontrar_ruta_mas_corta(graph, origen, destino):
    distancias = {nodo: float('inf') for nodo in graph}
    distancias[origen] = 0
    cola_prioridad = [(0, origen)]
    nodos_previos = {nodo: None for nodo in graph}
    
    while cola_prioridad:
        distancia_actual, nodo_actual = heapq.heappop(cola_prioridad)
        if nodo_actual == destino:
            break
        for vecino, peso in graph[nodo_actual]:
            nueva_distancia = distancia_actual + peso
            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                nodos_previos[vecino] = nodo_actual
                heapq.heappush(cola_prioridad, (nueva_distancia, vecino))

    camino = []
    actual = destino
    while actual:
        camino.append(actual)
        actual = nodos_previos[actual]
    camino = camino[::-1]

    if distancias[destino] == float('inf'):
        print(f"No hay ruta posible entre {origen} y {destino}.")
    else:
        print(f"Ruta más corta de {origen} a {destino}: {' -> '.join(camino)}")
        print(f"Distancia total: {distancias[destino]} km")

# Función para encontrar localidades con todas las distancias menores a 15 km
def localidades_con_distancias_cortas(graph, max_distancia):
    localidades_validas = []
    for localidad, conexiones in graph.items():
        if all(distancia < max_distancia for _, distancia in conexiones):
            localidades_validas.append(localidad)
    return localidades_validas

# Función para verificar si el grafo es conexo
def es_grafo_conexo(graph):
    visitados = set()
    def bfs(origen):
        cola = [origen]
        while cola:
            nodo = cola.pop(0)
            if nodo not in visitados:
                visitados.add(nodo)
                cola.extend(vecino for vecino, _ in graph[nodo] if vecino not in visitados)
    nodo_inicial = next(iter(graph))
    bfs(nodo_inicial)
    return len(visitados) == len(graph)

# Función para encontrar todas las rutas posibles sin ciclos entre dos localidades
def encontrar_todas_las_rutas(graph, origen, destino):
    rutas = []
    def bfs_rutas(camino_actual):
        ultima_localidad = camino_actual[-1]
        if ultima_localidad == destino:
            rutas.append(camino_actual)
            return
        for vecino, _ in graph[ultima_localidad]:
            if vecino not in camino_actual:
                bfs_rutas(camino_actual + [vecino])
    bfs_rutas([origen])
    if rutas:
        print(f"Todas las rutas posibles de {origen} a {destino} sin ciclos:")
        for i, ruta in enumerate(rutas, 1):
            print(f"Ruta {i}: {' -> '.join(ruta)}")
    else:
        print(f"No hay rutas posibles de {origen} a {destino}.")

# Función para calcular la ruta más larga sin ciclos entre dos localidades
def encontrar_ruta_mas_larga(graph, origen, destino):
    ruta_mas_larga = []
    max_distancia = 0
    def dfs(camino_actual, distancia_actual):
        nonlocal ruta_mas_larga, max_distancia
        ultima_localidad = camino_actual[-1]
        if ultima_localidad == destino:
            if distancia_actual > max_distancia:
                max_distancia = distancia_actual
                ruta_mas_larga = camino_actual[:]
            return
        for vecino, peso in graph[ultima_localidad]:
            if vecino not in camino_actual:
                dfs(camino_actual + [vecino], distancia_actual + peso)
    dfs([origen], 0)
    if ruta_mas_larga:
        print(f"Ruta más larga de {origen} a {destino} sin ciclos: {' -> '.join(ruta_mas_larga)}")
        print(f"Distancia total: {max_distancia} km")
    else:
        print(f"No hay rutas posibles de {origen} a {destino}.")

# Grafo de localidades
localidades = {
    "Madrid": [("Alcorcón", 13), ("Villaviciosa de Odón", 22), ("Alcalá de Henares", 35)],
    "Villanueva de la Cañada": [("Villaviciosa de Odón", 11), ("Boadilla del Monte", 7)],
    "Alcorcón": [("Madrid", 13), ("Móstoles", 5)],
    "Móstoles": [("Alcorcón", 5), ("Fuenlabrada", 8)],
    "Fuenlabrada": [("Móstoles", 8), ("Getafe", 10)],
    "Getafe": [("Fuenlabrada", 10), ("Madrid", 16)],
    "Villaviciosa de Odón": [("Madrid", 22), ("Villanueva de la Cañada", 11)],
    "Boadilla del Monte": [("Villanueva de la Cañada", 7), ("Madrid", 15)],
    "Alcalá de Henares": [("Madrid", 35), ("Torrejón de Ardoz", 15)],
    "Torrejón de Ardoz": [("Alcalá de Henares", 15), ("Madrid", 20)]
}

# Llamadas a las funciones
print("Ruta más corta:")
encontrar_ruta_mas_corta(localidades, "Madrid", "Móstoles")

print("\nLocalidades con todas las distancias menores a 15 km:")
localidades_validas = localidades_con_distancias_cortas(localidades, 15)
print(", ".join(localidades_validas) if localidades_validas else "Ninguna localidad cumple el criterio.")

print("\n¿Es el grafo conexo?")
print("Sí" if es_grafo_conexo(localidades) else "No")

print("\nTodas las rutas posibles sin ciclos:")
encontrar_todas_las_rutas(localidades, "Madrid", "Móstoles")

print("\nRuta más larga posible sin ciclos:")
encontrar_ruta_mas_larga(localidades, "Madrid", "Móstoles")
