class Maze:
    """
    Resuelve un laberinto usando algoritmo de backtracking.
    0 = pasillo (camino válido)
    1 = pared (obstáculo)
    """

    def __init__(self, matrix=None, start=None, goal=None):
        """
        Inicializa el laberinto con matriz, punto de inicio y objetivo.
        Si no se proporcionan parámetros, usa valores por defecto.
        """
        self.matrix = matrix
        
        # Calcula dimensiones de la matriz
        self.num_rows = len(self.matrix)
        self.num_columns = len(self.matrix[0])
        
        # Define punto de inicio y objetivo (esquina inferior derecha por defecto)
        self.start = start if start else (0, 0)
        self.goal = goal if goal else (self.num_rows-1, self.num_columns-1)
        
        # Registra todo el recorrido explorado (incluyendo backtrack)
        self.complete_path = []
        
        # Indica si se encontró un camino válido hasta el objetivo
        self.success = False


    def solve(self):
        """Inicia la búsqueda del camino desde el punto de inicio."""
        if self.backtracking_(self.start):
            self.success = True

    def get_choices(self, position):
        """
        Retorna todas las posiciones válidas (dentro de la matriz) 
        adyacentes a la posición actual.
        """
        y = int(position[0])  # fila (eje vertical)
        x = int(position[1])  # columna (eje horizontal)
        actions = []

        # Derecha: aumentar columna
        if (x + 1) < self.num_columns: 
            actions.append((y, x+1))

        # Izquierda: disminuir columna
        if x - 1 >= 0:
            actions.append((y, x-1))
            
        # Abajo: aumentar fila
        if y + 1 < self.num_rows:
            actions.append((y+1, x))
        
        # Arriba: disminuir fila
        if y - 1 >= 0:
            actions.append((y-1, x))

        return actions
        
    def backtracking_(self, position, path=None, visited=None):
        """
        Busca recursivamente un camino desde 'position' hasta el objetivo.
        
        Estrategia:
        1. Marca la posición como visitada (evita ciclos)
        2. Si es el objetivo, retorna True (solución encontrada)
        3. Prueba cada opción válida (no es pared, no visitada)
        4. Si alguna opción lleva a solución, retorna True
        5. Si ninguna funciona (dead end), deshace el movimiento y retorna False
        """
        # Inicializa estructuras si es la primera llamada
        if path is None:
            path = []
        if visited is None:
            visited = set()
        
        # PASO 1: Hacer la elección - añadir posición actual al camino
        path.append(position)
        visited.add(position)
        self.complete_path.append(position)  # Registra todo el recorrido
        
        # PASO 2: Condición base - verificar si llegamos al objetivo
        if position == self.goal:
            return True
        
        # PASO 3: Explorar - probar todas las opciones disponibles
        choices = self.get_choices(position)
        for choice in choices:
            # Saltar si es pared (1) o ya fue visitada
            if self.matrix[choice[0]][choice[1]] == 1 or choice in visited:
                continue
            
            # Recursión: intentar continuar desde esta opción
            if self.backtracking_(choice, path, visited):
                return True  # Este camino lleva a la solución
        
        # PASO 4: Deshacer (backtrack) - si ninguna opción funcionó
        # Limpiamos solo 'path' para que quede solo la ruta final exitosa, y en path_complete no para que muestre toda la trayectoria
        path.pop()
        return False
    
#--------------------------------------
def leer_laberinto():
    while True:
        try:
            M = int(input("Filas del laberinto: "))
            N = int(input("Columnas del laberinto: "))
            if M <= 0 or N <= 0:
                print("Las filas y columnas deben ser mayores que 0")
                continue
            break
        except ValueError:
            print("Ingresa un número entero válido para filas y columnas.")

    matrix = []
    print("Ingresa cada fila separando los números por espacio (0=pasillo, 1=pared):")
    for i in range(M):
        while True:
            fila_input = input(f"Fila {i+1}: ").strip().split()

            if len(fila_input) != N:
                print(f"Error: la fila debe tener exactamente {N} valores.")
                continue

            try:
                fila = [int(x) for x in fila_input]
                if any(x not in (0, 1) for x in fila):
                    print("Error: solo se permiten 0 y 1 en el laberinto.")
                    continue
            except ValueError:
                print("Error: todos los valores deben ser números enteros (0 o 1).")
                continue

            matrix.append(fila)
            break

    return matrix


def main():
    """Ejecuta el algoritmo de backtracking y muestra los resultados."""
    laberinto_usuario = leer_laberinto()
    maze = Maze(matrix=laberinto_usuario)
    maze.solve()
    
    # Muestra si se encontró solución
    if maze.success:
        print("✓ Camino encontrado hasta el objetivo:")
    else:
        print("✗ No se pudo llegar al objetivo, pero se exploró:")

    # Imprime todo el recorrido (incluye backtrack)
    tup = (1,1)
    print(" -> ".join(str(tuple(a + b for a,b in zip(p,tup))) for p in maze.complete_path))

if __name__ == "__main__":
    main()