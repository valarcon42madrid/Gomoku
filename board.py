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

    def get_empty_positions(self):
        """
        Devuelve una lista de todas las posiciones vacías en el tablero.
        :return: Lista de tuplas (fila, columna) para las posiciones vacías.
        """
        empty_positions = []
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == ".":
                    empty_positions.append((row, col))
        return empty_positions

    def undo_move(self, move):
        """
        Revierte un movimiento en el tablero.
        :param move: Una tupla (fila, columna) que indica el movimiento a deshacer.
        """
        row, col = move
        if 0 <= row < self.size and 0 <= col < self.size:
            self.grid[row][col] = "."

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

    def make_move_nocap(self, move, symbol):
        """
        Intenta realizar un movimiento en el tablero.
        :param move: (fila, columna)
        :param symbol: símbolo del jugador ('X' o 'O')
        :return: True si el movimiento es válido, False si no lo es.
        """
        row, col = move
        if self.is_valid_move(move, symbol):
            self.grid[row][col] = symbol
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

    def ft_notcap(self, row, col, dr, dc, symbol):
        """
        Comprueba si alguna ficha de la alineación ganadora puede ser capturada en cualquier dirección.
        :param row: fila inicial de la alineación
        :param col: columna inicial de la alineación
        :param r: fila final de la alineación
        :param c: columna final de la alineación
        :param dr: dirección de fila del incremento
        :param dc: dirección de columna del incremento
        :param symbol: símbolo del jugador ('X' o 'O')
        :return: False si alguna ficha puede ser capturada, True si ninguna puede serlo.
        """
    
        o_symbol = "X" if symbol == "O" else "O"

        directions = [
            (1, 0),  # Vertical
            (0, 1),  # Horizontal
            (1, 1),  # Diagonal descendente
            (1, -1), # Diagonal ascendente
            (-1, 0),
            (0, -1),
            (-1, 1),
            (-1, -1)
        ]

        for step in range(5):  # Revisar las 5 fichas en la alineación
            check_row = row + dr * step
            check_col = col + dc * step

            # Para cada ficha, comprobar en todas las direcciones posibles
            for ddr, ddc in directions:
                # Coordenadas en los extremos de la configuración
                prev_r, prev_c = check_row - ddr, check_col - ddc  # Anterior al símbolo
                next_r, next_c = check_row + ddr * 2, check_col + ddc * 2  # Espacio vacío al final

                # Coordenadas de los dos símbolos centrales
                mid_r1, mid_c1 = check_row, check_col
                mid_r2, mid_c2 = check_row + ddr, check_col + ddc
                
                print(self.grid[prev_r][prev_c] + " " + self.grid[mid_r1][mid_c1] + " " + self.grid[mid_r2][mid_c2] + " " + self.grid[next_r][next_c])
                # Verificar si la configuración es "enemy + symbol + symbol + espacio"
                if (
                    self.grid[prev_r][prev_c] == o_symbol
                    and self.grid[mid_r1][mid_c1] == symbol
                    and self.grid[mid_r2][mid_c2] == symbol
                    and self.grid[next_r][next_c] == "."
                ):
                    return False  # Una ficha es capturable
                if (
                    self.grid[prev_r][prev_c] == "."
                    and self.grid[mid_r1][mid_c1] == symbol
                    and self.grid[mid_r2][mid_c2] == symbol
                    and self.grid[next_r][next_c] == o_symbol
                ):
                    return False
        return True  # Ninguna ficha es capturable


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
                    if count == 5 and self.ft_notcap(row, col, dr, dc, symbol):
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
