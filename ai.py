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
        Determina el mejor movimiento para la IA siguiendo las reglas especificadas.
        :param board: Instancia del tablero (clase Board).
        :return: Una tupla (fila, columna) que representa el movimiento elegido.
        """
        # 1. Ganar si es posible
        move = self.find_alignment(board, self.symbol, 4, to_win=True)
        if move:
            return move

        # 2. Bloquear amenazas del oponente
        opponent_symbol = "X" if self.symbol == "O" else "O"
        for length in [5]:
            move = self.find_blocking_move_pro(board, opponent_symbol, length)
            if move:
                return move

        # 3. Capturar dos fichas enemigas
        move = self.find_capture_move(board)
        if move:
            return move

        for length in [4, 3, 2]:
            move = self.find_blocking_move_pro(board, opponent_symbol, length)
            if move:
                return move
            
        # 4 y 5. Bloquear extremos de alineaciones enemigas
        for length in [3, 2]:
            move = self.block_alignment_extremes(board, opponent_symbol, length)
            if move:
                return move

        # 6. Aplicar heurística minimax
        _, move = self.minimax(board, depth=2, maximizing_player=True)
        if move:
            return move

        # 7. Colocar cerca de fichas enemigas
        move = self.near_opponent(board, opponent_symbol)
        if move:
            return move

        # Movimiento predeterminado
        return random.choice(board.get_empty_positions())

    def find_alignment(self, board, symbol, length, to_win=False):
        """
        Busca alineaciones propias o del oponente. Considera casos de alineaciones
        peligrosas con espacios intermedios o extremos abiertos.
        :param board: Instancia del tablero (clase Board).
        :param symbol: Símbolo a buscar en la alineación.
        :param length: Longitud de la alineación a buscar.
        :param to_win: Si es True, busca ganar; si es False, busca bloquear.
        :return: Coordenadas (fila, columna) del mejor movimiento, o None.
        """
        directions = [(1, 0), (0, 1), (1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1), (-1, 1)]
        for row in range(board.size):
            for col in range(board.size):
                if board.grid[row][col] != ".":
                    continue
                for dr, dc in directions:
                    aligned_count = 0
                    gaps = 0
                    positions = []  # Para almacenar las posiciones alineadas y huecos

                    for step in range(-length, length + 1):
                        r, c = row + dr * step, col + dc * step
                        if 0 <= r < board.size and 0 <= c < board.size:
                            if board.grid[r][c] == symbol:
                                aligned_count += 1
                                positions.append((r, c))
                            elif board.grid[r][c] == ".":
                                gaps += 1
                                positions.append((r, c))
                            else:
                                # Otro símbolo bloquea la alineación
                                break
                        else:
                            # Fuera del tablero, bloquea la alineación
                            break

                    # Verificar condiciones para ganar o bloquear
                    if (
                        aligned_count == length
                        and (gaps == 1 or to_win)  # Considera un hueco si no es para ganar
                        and (row, col) in positions  # El espacio actual es parte del patrón
                    ):
                        return row, col

                    # Detectar peligros por extremos
                    if (
                        aligned_count == length - 1
                        and gaps == 2
                        and (row, col) in positions  # Asegurarse de que es parte del patrón
                    ):
                        start_r, start_c = row - dr, col - dc
                        end_r, end_c = row + dr, col + dc
                        if (
                            0 <= start_r < board.size and 0 <= start_c < board.size and board.grid[start_r][start_c] == "."
                            and 0 <= end_r < board.size and 0 <= end_c < board.size and board.grid[end_r][end_c] == "."
                        ):
                            return row, col

        return None


    def find_blocking_move_pro(self, board, opponent_symbol, length):
        """
        Encuentra movimientos para bloquear alineaciones enemigas.
        """
        return self.find_alignment(board, opponent_symbol, length, to_win=True)
    
    def find_blocking_move(self, board, opponent_symbol, length):
        """
        Encuentra movimientos para bloquear alineaciones enemigas.
        """
        return self.find_alignment(board, opponent_symbol, length, to_win=False)

    def find_capture_move(self, board):
        # Encuentra un movimiento que capture piezas del oponente
        opponent_symbol = "X" if self.symbol == "O" else "O"
        directions = [(1, 0), (0, 1), (1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1), (-1, 1)]

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

    def block_alignment_extremes(self, board, opponent_symbol, length):
        """
        Bloquea los extremos de alineaciones enemigas.
        """
        directions = [(1, 0), (0, 1), (1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1), (-1, 1)]
        for row in range(board.size):
            for col in range(board.size):
                if board.grid[row][col] != ".":
                    continue
                for dr, dc in directions:
                    aligned = []
                    for step in range(length):
                        r, c = row + dr * step, col + dc * step
                        if 0 <= r < board.size and 0 <= c < board.size:
                            if board.grid[r][c] == opponent_symbol:
                                aligned.append((r, c))
                    if len(aligned) == length:
                        return row, col
        return None

    def minimax(self, board, depth, maximizing_player):
        """
        Algoritmo minimax para evaluar movimientos.
        """
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board), None

        best_move = None
        if maximizing_player:
            max_eval = float('-inf')
            for move in board.get_empty_positions():
                board.make_move_nocap(move, self.symbol)
                eval_score, _ = self.minimax(board, depth - 1, False)
                board.undo_move(move)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
            return max_eval, best_move
        else:
            opponent_symbol = "X" if self.symbol == "O" else "O"
            min_eval = float('inf')
            for move in board.get_empty_positions():
                board.make_move_nocap(move, opponent_symbol)
                eval_score, _ = self.minimax(board, depth - 1, True)
                board.undo_move(move)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
            return min_eval, best_move

    def near_opponent(self, board, opponent_symbol):
        """
        Busca un movimiento cerca de fichas enemigas.
        """
        for row in range(board.size):
            for col in range(board.size):
                if board.grid[row][col] == opponent_symbol:
                    directions = [(1, 0), (0, 1), (1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1), (-1, 1)]
                    for dr, dc in directions:
                        r, c = row + dr, col + dc
                        if 0 <= r < board.size and 0 <= c < board.size and board.grid[r][c] == ".":
                            return r, c
        return None

    def evaluate_board(self, board):
        """
        Evalúa el tablero para determinar la ventaja.
        """
        score = 0
        opponent_symbol = "X" if self.symbol == "O" else "O"
        for row in range(board.size):
            for col in range(board.size):
                if board.grid[row][col] == self.symbol:
                    score += 10
                elif board.grid[row][col] == opponent_symbol:
                    score -= 10
        return score
