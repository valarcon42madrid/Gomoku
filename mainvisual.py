import pygame
from board import Board
from player import Player
from ai import AIPlayer

# Constantes de Pygame
WINDOW_SIZE = 600
BOARD_SIZE = 19
CELL_SIZE = WINDOW_SIZE // BOARD_SIZE
LINE_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (200, 200, 200)
HUMAN_COLOR = (0, 0, 255)
AI_COLOR = (255, 0, 0)
BUTTON_COLOR = (100, 200, 100)
TEXT_COLOR = (255, 255, 255)

class GomokuPygame:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Gomoku")
        self.clock = pygame.time.Clock()

        # Configuración del juego
        self.board = Board(BOARD_SIZE)
        self.human_player = Player("Humano", "X")
        self.ai_player = AIPlayer("IA", "O")
        self.current_player = self.human_player
        self.mode = None  # Modo de juego: 1 = Humano vs IA, 2 = Humano vs Humano

    def get_cell_from_mouse(self, pos):
        """
        Obtiene la celda (fila, columna) basada en la posición del mouse.
        :param pos: Posición del mouse (x, y).
        :return: Tupla (fila, columna).
        """
        x, y = pos
        return y // CELL_SIZE, x // CELL_SIZE
    
    def handle_human_turn(self, pos):
        """
        Maneja el turno del jugador humano.
        :param pos: Posición del mouse.
        """
        row, col = self.get_cell_from_mouse(pos)
        if self.board.is_valid_move((row, col), self.human_player.symbol):
            self.board.make_move((row, col), self.human_player.symbol)
            if self.board.check_winner(self.human_player.symbol):
                self.show_message("¡Humano gana!")
                pygame.quit()
                exit()

            self.current_player = self.ai_player

    def handle_human_turn_two(self, pos):
        """
        Maneja el turno del jugador humano.
        :param pos: Posición del mouse.
        """
        row, col = self.get_cell_from_mouse(pos)
        if self.board.is_valid_move((row, col), "O"):
            self.board.make_move((row, col), "O")
            if self.board.check_winner("O"):
                self.show_message("¡Humano 2 gana!")
                pygame.quit()
                exit()

            self.current_player = self.human_player

    def handle_ai_turn(self):
        """
        Maneja el turno de la IA.
        """
        row, col = self.ai_player.get_best_move(self.board)
        self.board.make_move((row, col), self.ai_player.symbol)
        if self.board.check_winner(self.ai_player.symbol):
            self.show_message("¡IA gana!")
            pygame.quit()
            exit()

        self.current_player = self.human_player

    def show_message(self, message):
        """
        Muestra un mensaje emergente con el resultado del juego.
        :param message: Mensaje a mostrar.
        """
        self.draw_board()
        pygame.display.flip()
        pygame.time.wait(1000)
        font = pygame.font.Font(None, 74)
        text = font.render(message, True, (255, 0, 0))
        self.window.fill(BACKGROUND_COLOR)
        self.window.blit(text, (WINDOW_SIZE // 6, WINDOW_SIZE // 2))
        pygame.display.update()
        pygame.time.wait(3000)

    def draw_board(self):
        """
        Dibuja el tablero en la ventana de Pygame.
        """
        self.window.fill(BACKGROUND_COLOR)

        # Dibujar líneas del tablero
        for i in range(BOARD_SIZE):
            pygame.draw.line(
                self.window, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, WINDOW_SIZE)
            )
            pygame.draw.line(
                self.window, LINE_COLOR, (0, i * CELL_SIZE), (WINDOW_SIZE, i * CELL_SIZE)
            )

        # Dibujar las piezas
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                symbol = self.board.grid[row][col]
                if symbol == "X":
                    pygame.draw.circle(
                        self.window,
                        HUMAN_COLOR,
                        (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                        CELL_SIZE // 3,
                    )
                elif symbol == "O":
                    pygame.draw.circle(
                        self.window,
                        AI_COLOR,
                        (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                        CELL_SIZE // 3,
                    )

    def draw_menu(self):
        """
        Dibuja el menú inicial para seleccionar el modo de juego.
        """
        self.window.fill(BACKGROUND_COLOR)
        font = pygame.font.Font(None, 74)

        # Botón 1: Humano vs IA
        button_1 = pygame.Rect(WINDOW_SIZE // 4, WINDOW_SIZE // 3, WINDOW_SIZE // 2, 50)
        pygame.draw.rect(self.window, BUTTON_COLOR, button_1)
        text_1 = font.render("Humano vs IA", True, TEXT_COLOR)
        self.window.blit(text_1, (button_1.x + 20, button_1.y + 5))

        # Botón 2: Humano vs Humano
        button_2 = pygame.Rect(WINDOW_SIZE // 4, WINDOW_SIZE // 2, WINDOW_SIZE // 2, 50)
        pygame.draw.rect(self.window, BUTTON_COLOR, button_2)
        text_2 = font.render("Humano vs Humano", True, TEXT_COLOR)
        self.window.blit(text_2, (button_2.x + 5, button_2.y + 5))

        pygame.display.flip()
        return button_1, button_2

    def handle_menu_click(self, pos, button_1, button_2):
        """
        Maneja el clic en el menú inicial.
        """
        if button_1.collidepoint(pos):
            return 1  # Modo Humano vs IA
        elif button_2.collidepoint(pos):
            return 2  # Modo Humano vs Humano
        return None

    def run(self):
        """
        Corre el bucle principal del juego.
        """
        # Pantalla de selección de modo de juego
        button_1, button_2 = self.draw_menu()

        while self.mode is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mode = self.handle_menu_click(event.pos, button_1, button_2)

        # Bucle principal del juego
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and self.current_player == self.human_player:
                    self.handle_human_turn(event.pos)

            # Si es el turno de la IA
            if self.current_player == self.ai_player and self.mode == 1:
                self.handle_ai_turn()
            elif event.type == pygame.MOUSEBUTTONDOWN and self.current_player == self.ai_player:
                self.handle_human_turn_two(event.pos)

            # Dibujar el tablero
            self.draw_board()
            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()


if __name__ == "__main__":
    game = GomokuPygame()
    game.run()


