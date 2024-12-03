class Player:
    def __init__(self, name, symbol):
        """
        Inicializa al jugador.
        :param name: Nombre del jugador.
        :param symbol: Símbolo del jugador ('X' o 'O').
        """
        self.name = name
        self.symbol = symbol

    def get_move(self, board):
        """
        Solicita al jugador humano un movimiento válido.
        :param board: Instancia del tablero (clase Board).
        :return: Una tupla (fila, columna) que representa el movimiento del jugador.
        """
        while True:
            try:
                move = input(f"{self.name}, ingresa tu movimiento (fila,columna): ")
                row, col = map(int, move.split(","))
                # Pasar el símbolo del jugador al método is_valid_move
                if board.is_valid_move((row, col), self.symbol):
                    return row, col
                else:
                    print("Movimiento inválido. Asegúrate de que la celda está vacía y dentro del rango.")
            except (ValueError, IndexError):
                print("Entrada inválida. Por favor, ingresa el movimiento en el formato fila,columna (ejemplo: 3,4).")