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
        Calcula el mejor movimiento basado en prioridades especificadas.
        :param board: Instancia del tablero (clase Board).
        :return: Una tupla (fila, columna) que representa el movimiento elegido por la IA.
        """
        # Prioridad 1: Jugadas que ganan
        winning_move = self.find_winning_move(board)
        if winning_move:
            return winning_move

        # Prioridad 2: Bloquear alineaciones enemigas de 4 consecutivas
        block_four_move = self.find_block_move(board, length=4)
        if block_four_move:
            return block_four_move

        # Prioridad 3: Generar alineaciones de 4 abiertas
        create_open_four = self.create_open_alignment(board, length=4)
        if create_open_four:
            return create_open_four

        # Prioridad 4: Jugadas que capturan
        capture_move = self.find_capture_move(board)
        if capture_move:
            return capture_move

        # Prioridad 5: Bloquear alineaciones enemigas de 3 consecutivas
        block_three_move = self.find_block_move(board, length=3)
        if block_three_move:
            return block_three_move

        # Prioridad 6: Alinear 4 abiertas por 1 lado o 3 abiertas por ambos lados
        strategic_alignment = self.create_partial_alignment(board)
        if strategic_alignment:
            return strategic_alignment

        # Prioridad 7: Evaluar con Minimax
        _, best_move = self.minimax(board, depth=2, maximizing_player=True)
        if best_move:
            return best_move

        # Prioridad 8: Jugar en esquinas
        corner_move = self.find_corner_move(board)
        if corner_move:
            return corner_move

        # Prioridad 9: Jugar en los bordes
        edge_move = self.find_edge_move(board)
        if edge_move:
            return edge_move

        # Default: Movimiento aleatorio
        return random.choice(board.get_empty_positions())

    def find_winning_move(self, board):
        # Busca movimientos que permitan ganar
        return self.find_specific_alignment(board, self.symbol, 4, to_win=True)

    def find_block_move(self, board, length):
        # Busca movimientos que bloqueen alineaciones del oponente
        opponent_symbol = "X" if self.symbol == "O" else "O"
        return self.find_specific_alignment(board, opponent_symbol, length, to_win=False)

    def find_capture_move(self, board):
        # Encuentra un movimiento que capture piezas del oponente
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

    def create_open_alignment(self, board, length):
        # Genera alineaciones abiertas de la longitud especificada
        return self.find_specific_alignment(board, self.symbol, length, open_ends=2)

    def create_partial_alignment(self, board):
        # Genera alineaciones de 4 abiertas por un lado o 3 abiertas por ambos lados
        partial_four = self.find_specific_alignment(board, self.symbol, 4, open_ends=1)
        if partial_four:
            return partial_four
        return self.find_specific_alignment(board, self.symbol, 3, open_ends=2)

    def find_specific_alignment(self, board, symbol, length, to_win=False, open_ends=0):
        # Encuentra movimientos que logren una alineación específica
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        for row in range(board.size):
            for col in range(board.size):
                if board.grid[row][col] != ".":
                    continue
                for dr, dc in directions:
                    aligned_count = 0
                    open_count = 0
                    for step in range(-length, length + 1):
                        r, c = row + dr * step, col + dc * step
                        if 0 <= r < board.size and 0 <= c < board.size:
                            if board.grid[r][c] == symbol:
                                aligned_count += 1
                            elif board.grid[r][c] == ".":
                                open_count += 1
                        else:
                            break

                    if aligned_count == length and (open_count >= open_ends or to_win):
                        return row, col
        return None

    def find_corner_move(self, board):
        # Encuentra movimientos en las esquinas
        corners = [(0, 0), (0, board.size - 1), (board.size - 1, 0), (board.size - 1, board.size - 1)]
        for corner in corners:
            if board.grid[corner[0]][corner[1]] == ".":
                return corner
        return None

    def find_edge_move(self, board):
        # Encuentra movimientos en los bordes
        for row in [0, board.size - 1]:
            for col in range(board.size):
                if board.grid[row][col] == ".":
                    return row, col
        for col in [0, board.size - 1]:
            for row in range(board.size):
                if board.grid[row][col] == ".":
                    return row, col
        return None

    def minimax(self, board, depth, maximizing_player):
        # Algoritmo Minimax simplificado
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board), None

        best_move = None

        if maximizing_player:
            max_eval = float('-inf')
            for move in board.get_empty_positions():
                board.make_move(move, self.symbol)
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
                board.make_move(move, opponent_symbol)
                eval_score, _ = self.minimax(board, depth - 1, True)
                board.undo_move(move)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
            return min_eval, best_move

    def evaluate_board(self, board):
        # Evalúa el tablero
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

