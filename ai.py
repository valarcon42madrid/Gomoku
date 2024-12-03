import random

class AIPlayer:
    def __init__(self, name, symbol):
        """
        Inicializa a la IA.
        :param name: Nombre de la IA.
        :param symbol: Símbolo de la IA ('X' o 'O').
        """
        self.name = name
        self.symbol = symbol

    def get_best_move(self, board):
        """
        Calcula el mejor movimiento basado en prioridades: ganar, capturar, bloquear, o evaluar con Minimax.
        :param board: Instancia del tablero (clase Board).
        :return: Una tupla (fila, columna) que representa el movimiento elegido por la IA.
        """
        # Prioridad 1: Jugadas que ganan
        winning_move = self.find_winning_move(board)
        if winning_move:
            return winning_move

        # Prioridad 2: Jugadas que capturan
        capture_move = self.find_capture_move(board)
        if capture_move:
            return capture_move

        # Prioridad 3: Bloquear alineaciones peligrosas del oponente
        block_move = self.find_block_move(board)
        if block_move:
            return block_move

        # Prioridad 4: Evaluar con Minimax
        _, best_move = self.minimax(board, depth=2, maximizing_player=True)
        return best_move

    def find_winning_move(self, board):
        """
        Encuentra un movimiento que permita ganar inmediatamente.
        :param board: Instancia del tablero.
        :return: Una tupla (fila, columna) o None si no hay movimientos ganadores.
        """
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        for row in range(board.size):
            for col in range(board.size):
                if board.grid[row][col] != ".":
                    continue
                for dr, dc in directions:
                    count = 0
                    for step in range(-4, 5):  # Verificar 9 posiciones alrededor
                        r, c = row + dr * step, col + dc * step
                        if (
                            0 <= r < board.size
                            and 0 <= c < board.size
                            and board.grid[r][c] == self.symbol
                        ):
                            count += 1
                        else:
                            break
                    if count >= 4:  # Jugada que completa 5
                        return row, col
        return None

    def find_capture_move(self, board):
        """
        Encuentra un movimiento que capture piezas del oponente.
        :param board: Instancia del tablero.
        :return: Una tupla (fila, columna) o None si no hay movimientos de captura disponibles.
        """
        opponent_symbol = "X" if self.symbol == "O" else "O"
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        for row in range(board.size):
            for col in range(board.size):
                if board.grid[row][col] != ".":
                    continue
                for dr, dc in directions:
                    r1, c1 = row + dr, col + dc
                    r2, c2 = row + 2 * dr, col + 2 * dc
                    r3, c3 = row + 3 * dr, col + 3 * dc

                    if (
                        0 <= r1 < board.size
                        and 0 <= c1 < board.size
                        and 0 <= r2 < board.size
                        and 0 <= c2 < board.size
                        and 0 <= r3 < board.size
                        and 0 <= c3 < board.size
                        and board.grid[r1][c1] == opponent_symbol
                        and board.grid[r2][c2] == opponent_symbol
                        and board.grid[r3][c3] == self.symbol
                    ):
                        return row, col
        return None

    def find_block_move(self, board):
        """
        Encuentra un movimiento para bloquear alineaciones peligrosas del oponente.
        :param board: Instancia del tablero.
        :return: Una tupla (fila, columna) o None si no hay bloqueos necesarios.
        """
        opponent_symbol = "X" if self.symbol == "O" else "O"
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        for row in range(board.size):
            for col in range(board.size):
                if board.grid[row][col] != ".":
                    continue
                for dr, dc in directions:
                    aligned_count = 0
                    open_ends = 0
                    for step in range(-4, 5):  # Verificar alineaciones del oponente
                        r, c = row + dr * step, col + dc * step
                        if (
                            0 <= r < board.size
                            and 0 <= c < board.size
                            and board.grid[r][c] == opponent_symbol
                        ):
                            aligned_count += 1
                        elif (
                            0 <= r < board.size
                            and 0 <= c < board.size
                            and board.grid[r][c] == "."
                        ):
                            open_ends += 1
                        else:
                            break
                    if aligned_count >= 2 and open_ends >= 2:  # Bloquear alineaciones abiertas
                        return row, col
        return None

    def minimax(self, board, depth, maximizing_player):
        """
        Algoritmo Minimax simplificado con heurísticas.
        :param board: Instancia del tablero.
        :param depth: Profundidad máxima de búsqueda.
        :param maximizing_player: True si es el turno de la IA, False para el oponente.
        :return: Mejor puntuación y movimiento (row, col).
        """
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board), None

        best_move = None

        if maximizing_player:
            max_eval = float('-inf')
            for row in range(board.size):
                for col in range(board.size):
                    if board.is_valid_move((row, col), self.symbol):
                        board.make_move((row, col), self.symbol)
                        eval_score, _ = self.minimax(board, depth - 1, False)
                        board.grid[row][col] = "."  # Deshacer movimiento
                        if eval_score > max_eval:
                            max_eval = eval_score
                            best_move = (row, col)
            return max_eval, best_move
        else:
            opponent_symbol = "X" if self.symbol == "O" else "O"
            min_eval = float('inf')
            for row in range(board.size):
                for col in range(board.size):
                    if board.is_valid_move((row, col), opponent_symbol):
                        board.make_move((row, col), self.symbol)
                        eval_score, _ = self.minimax(board, depth - 1, True)
                        board.grid[row][col] = "."  # Deshacer movimiento
                        if eval_score < min_eval:
                            min_eval = eval_score
                            best_move = (row, col)
            return min_eval, best_move

    def evaluate_board(self, board):
        """
        Evalúa el estado del tablero basado en capturas y alineaciones simples.
        :param board: Instancia del tablero.
        :return: Puntuación del tablero desde la perspectiva de la IA.
        """
        score = 0
        opponent_symbol = "X" if self.symbol == "O" else "O"

        for row in range(board.size):
            for col in range(board.size):
                if board.grid[row][col] == self.symbol:
                    score += 10
                elif board.grid[row][col] == opponent_symbol:
                    score -= 10

        # Priorizar capturas
        score += board.captures[self.symbol] * 100
        score -= board.captures[opponent_symbol] * 100

        return score
