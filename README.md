Hex Game

Hex es un juego de mesa de suma 0 con "perfect information"

Tablero

Hex es jugado en un tablero hecho de hexágonos. El mismo tablero tiene forma de rombo, como se muestra en la imagen. 
Las fichas se sitúan en los hexágonos del tablero. El tablero mostrado aquí tiene 11 fichas a cada lado del rombo, lo cual es un tamaño común para jugadores experimentados, 
pero el juego puede ser jugado en tableros de cualquier tamaño.

Objetivo

El objetivo es hacer un camino con las fichas de tu color entre lados (del mismo color) opuestos del tablero. El jugador contrario intentara hacer una cadena entre los lados del otro color del tablero. 
La cadena no tiene que estar en línea recta, siempre que la cadena esté cerrada, es decir, las fichas se encuentran directamente una al lado de la otra. En el juego que se muestra a continuación, el azul ganó.

Definiciones

La información completa de este juego, y cualquier juego combinatorio, puede ser representado en una jerarquía llamada game-tree. Un árbol de juego tiene una raíz, la cual representa el estado de inicio de un juego y sus nodos son estados validos del tablero mientras que las aristas son movimientos o jugadas legales, en los que se llega de un estado del juego (nodo padre) hacia otro estado del juego (nodo hijo) después de aplicar el movimiento. El árbol representa la información completa del juego ya que tiene el conjunto completo de todas las posiciones del tablero. En un árbol de juego, un juego o partido es un único camino comenzando desde la raíz (estado inicial) y termina un una nodo hoja. Las representaciones de un tablero en los nodos hojas son llamados tablero terminal. Cada nivel del árbol representa las opciones de jugada de un jugador para ese turno.
Un jugador es un agente que dado un tablero, es capaz de generar la próxima jugada según algún criterio que lleve a la victoria.

Con este proyecto se implementa un jugador inteligente para el juego de Hex,basado en el algoritmo Minimax con poda alfa-beta para tomar decisiones estratégicas.
Minimax es un algoritmo recursivo el cual se usa para elegir un movimiento optimo para un jugador asumiendo que el oponente también jugara de manera optima. Como su nombre sugiere, su meta es minimizar la perdida máxima (minimizar el peor escenario).
Una búsqueda minimax es una búsqueda exhaustiva en profundidad de un árbol de juego que devuelve un valor "score". Una búsqueda minimax tiene dos fases llamadas fase de maximización y fase de minimización, respectivamente. La fase de maximización ocurre en todas las posiciones del tablero donde el primer jugador tiene el turno y la fase de minimización ocurre en todas las posiciones del tablero donde el segundo jugador tiene el turno. La fase de maximización devuelve el mayor score asignado a los sucesores mientras que la fase de minimización devuelve el valor más pequeño asignado a los sucesores
Los estados finales del tableros o nodos hojas se le asigna 1 si el primer jugador gana y -1 en caso contrario. A medida que la búsqueda hace backtrack desde las posiciones terminales, a los nodos en la fase de maximización se les asigna el valor más grande asignado a sus sucesores y a los nodos en la fase de minimización se les asigna el valor más pequeño asignado a sus sucesores. Entonces se selecciona el camino desde la raíz y el nodo hoja que represente la jugada con un mayor score en su camino.

La evaluación de posiciones se realiza mediante una función heurística que combina distancias mínimas (usando una versión adaptada del algoritmo de Dijkstra) con el conteo de "puentes" estratégicos.

Características principales
Poda Alfa-Beta: Mejora la eficiencia de Minimax descartando ramas que no pueden afectar la decisión final. 
Al buscar el árbol completo se crea un jugador que nuca pierde pues conoce completa todos los resultados posibles. Pero a diferencia del Tic Tac Toe que es un tablero pequeño, desplegar todas sus jugadas no es difícil en una maquina de computo. Pero para un juego como el Hex que normalmente se juega en tableros de 11x11, lo cual no es una opción. Por lo que agregamos una poda para reducir el número de nodos buscados, sin afectar su optimalidad.
El algoritmo de poda α-β es una extensión de la búsqueda por minimax que tiene dos valores alpha y beta que atan el 'score' en cada nodo o estado del juego. El valor de alpha es el menor valor atado al nodo el cual es maximizado en la búsqueda mientras que beta es el mayor y es minimizado en la búsqueda.
La poda es desencadenada por dos condiciones conocidas como condiciones de corte alpha y beta. Una condición de corte beta ocurre mientras se busca el nodo E. Ya que la búsqueda esta maximizando al nodo E y el valor de este es mayor o igual al valor beta de B, y como la búsqueda minimiza en el nodo B, la búsqueda en el nodo E nunca devolverá un valor menor del valor en el nodo B. Por ello, lo que queda por revisar del sub-árbol con raíz E se elimina de la búsqueda. De manera similar, una condición de corte alpha ocurre mientras se busca el nodo C. Ya que la búsqueda esta minimiza al nodo C y el valor de este es menor o igual al valor alpha de A, y como la búsqueda maximiza en el nodo A, la búsqueda en el nodo C nunca devolverá un valor mayor del valor en el nodo A. Por ello, lo que queda por revisar del sub-árbol con raíz C se elimina de la búsqueda.

Función de evaluación heurística:
Dijkstra adaptado: Calcula el costo mínimo para conectar los bordes que debe unir el jugador.
Conteo de puentes: Identifica posiciones clave que podrían facilitar futuras conexiones entre piezas propias.
Control dinámico de profundidad: Ajusta la profundidad de búsqueda dependiendo del estado de la partida (por ejemplo, al inicio se utiliza una profundidad menor para agilizar la respuesta).
Estrategia del jugador
Si existe una jugada ganadora inmediata, se prioriza.
En las primeras etapas de la partida, se realiza una búsqueda menos profunda para ahorrar recursos computacionales.
Al evaluar una posición:
Si se alcanza la profundidad máxima sin un ganador, la evaluación considera varios factores:
Mayor longitud del camino del oponente.
Menor longitud del camino del jugador.
Mayor cantidad de puentes del jugador.
Menor cantidad de puentes del oponente.
