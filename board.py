# board.py

class Board:
    def __init__(self, size):
        """Inicializa el tablero de juego."""
        self.size = size
        self.grid = [["." for _ in range(size)] for _ in range(size)]
        self.captures = {"X": 0, "O": 0}  # Capturas acumuladas por cada jugador

    def display(self):
        """Muestra el tablero en la consola."""
        print("\n  " + " ".join([str(i).rjust(2) for i in range(self.size)]))
        for idx, row in enumerate(self.grid):
            print(f"{str(idx).rjust(2)} " + " ".join(row))
        print()
        print(f"Capturas: X = {self.captures['X']}, O = {self.captures['O']}")

    def make_move(self, move, symbol):
        """
        Intenta realizar un movimiento en el tablero.
        :param move: (fila, columna)
        :param symbol: símbolo del jugador ('X' o 'O')
        :return: True si el movimiento es válido, False si no lo es.
        """
        row, col = move
        if self.is_valid_move(move, symbol):
            self.grid[row][col] = symbol
            self.check_and_execute_capture(row, col, symbol)  # Verificar si ocurre captura
            return True
        return False

    def check_winner(self, symbol):
        """
        Comprueba si el símbolo dado ha ganado por alineación o captura.
        :param symbol: símbolo del jugador ('X' o 'O')
        :return: True si hay un ganador, False en caso contrario.
        """
        # Victoria por captura
        if self.captures[symbol] >= 10:
            return True

        # Victoria por alineación
        if self.has_alignment(symbol):
            opponent_symbol = "X" if symbol == "O" else "O"
            if self.captures[opponent_symbol] >= 8:  # Condición de Endgame Capture
                return False
            return True

        return False

    def has_alignment(self, symbol):
        """
        Comprueba si un jugador tiene una alineación de 5 consecutivas.
        :param symbol: símbolo del jugador ('X' o 'O')
        :return: True si hay alineación, False en caso contrario.
        """
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # Vertical, horizontal, diagonal
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] != symbol:
                    continue
                for dr, dc in directions:
                    count = 0
                    for step in range(5):  # Chequear 5 posiciones consecutivas
                        r, c = row + dr * step, col + dc * step
                        if (
                            0 <= r < self.size
                            and 0 <= c < self.size
                            and self.grid[r][c] == symbol
                        ):
                            count += 1
                        else:
                            break
                    if count == 5:
                        return True
        return False

    def is_valid_move(self, move, symbol):
        
        row, col = move
        if not (0 <= row < self.size and 0 <= col < self.size):
            return False
        if self.grid[row][col] != ".":
            return False

    # Comprobar la regla de "No doble tres"
        if self.introduces_double_threes(row, col, symbol):
            return False
        return True
    
    def introduces_double_threes(self, row, col, symbol):
        """
        Comprueba si un movimiento introduce dos alineaciones de tres abiertas (doble tres).
        :param row: Fila del movimiento.
        :param col: Columna del movimiento.
        :param symbol: Símbolo del jugador ('X' o 'O').
        :return: True si el movimiento crea un doble tres, False en caso contrario.
        """
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # Vertical, horizontal, diagonal
        open_threes = 0

        for dr, dc in directions:
            count = 1  # Incluye la posición actual
            open_ends = 0

            for step in range(1, 5):  # Hacia adelante
                r, c = row + dr * step, col + dc * step
                if 0 <= r < self.size and 0 <= c < self.size:
                    if self.grid[r][c] == symbol:
                        count += 1
                    elif self.grid[r][c] == ".":
                        open_ends += 1
                        break
                    else:
                        break

            for step in range(1, 5):  # Hacia atrás
                r, c = row - dr * step, col - dc * step
                if 0 <= r < self.size and 0 <= c < self.size:
                    if self.grid[r][c] == symbol:
                        count += 1
                    elif self.grid[r][c] == ".":
                        open_ends += 1
                        break
                    else:
                        break

            if count == 3 and open_ends == 2:  # Verifica un tres abierto
                open_threes += 1

        return open_threes >= 2

    def check_and_execute_capture(self, row, col, symbol):
        """
        Verifica y ejecuta capturas si se encuentran pares del oponente flanqueados.
        :param row: Fila del movimiento.
        :param col: Columna del movimiento.
        :param symbol: Símbolo del jugador que realizó el movimiento.
        """
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # Vertical, horizontal, diagonales
        opponent_symbol = "X" if symbol == "O" else "O"

        for dr, dc in directions:
            # Posiciones a verificar hacia adelante
            r1, c1 = row + dr, col + dc
            r2, c2 = row + 2 * dr, col + 2 * dc
            r3, c3 = row + 3 * dr, col + 3 * dc

            if (
                0 <= r1 < self.size
                and 0 <= c1 < self.size
                and 0 <= r2 < self.size
                and 0 <= c2 < self.size
                and 0 <= r3 < self.size
                and 0 <= c3 < self.size
                and self.grid[r1][c1] == opponent_symbol
                and self.grid[r2][c2] == opponent_symbol
                and self.grid[r3][c3] == symbol
            ):
                # Captura identificada hacia adelante
                self.grid[r1][c1] = "."
                self.grid[r2][c2] = "."
                self.captures[symbol] += 2

            # Posiciones a verificar hacia atrás
            r1, c1 = row - dr, col - dc
            r2, c2 = row - 2 * dr, col - 2 * dc
            r3, c3 = row - 3 * dr, col - 3 * dc

            if (
                0 <= r1 < self.size
                and 0 <= c1 < self.size
                and 0 <= r2 < self.size
                and 0 <= c2 < self.size
                and 0 <= r3 < self.size
                and 0 <= c3 < self.size
                and self.grid[r1][c1] == opponent_symbol
                and self.grid[r2][c2] == opponent_symbol
                and self.grid[r3][c3] == symbol
            ):
                # Captura identificada hacia atrás
                self.grid[r1][c1] = "."
                self.grid[r2][c2] = "."
                self.captures[symbol] += 2


    def is_game_over(self):
        """
        Comprueba si el juego ha terminado.
        :return: True si hay un ganador o si el tablero está lleno.
        """
        # Comprobar victoria por alineación o capturas
        if self.captures["X"] >= 10 or self.captures["O"] >= 10:
            return True

        if self.check_winner("X") or self.check_winner("O"):
            return True

        # Comprobar si el tablero está lleno
        return self.is_draw()

    def is_draw(self):
        """
        Comprueba si el tablero está lleno y no hay ganador.
        :return: True si el tablero está lleno y no hay ganador.
        """
        return all(cell != "." for row in self.grid for cell in row)
