
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
        pygame.display.flip()
        font = pygame.font.Font(None, 74)
        text = font.render(message, True, (255, 0, 0))
        self.window.fill(BACKGROUND_COLOR)
        self.window.blit(text, (WINDOW_SIZE // 6, WINDOW_SIZE // 2))
        pygame.display.update()
        pygame.time.wait(3000)

    def run(self):
        """
        Corre el bucle principal del juego.
        """
        print("¡Bienvenido al juego de Gomoku!")
        print("Selecciona el modo de juego:")
        print("1. Humano vs. IA")
        print("2. Humano vs. Humano")

        while True:
            try:
                mode = int(input("Elige 1 o 2: "))
                if mode in [1, 2]:
                    break
                else:
                    print("Por favor, ingresa 1 o 2.")
            except ValueError:
                print("Entrada inválida. Por favor, ingresa 1 o 2.")

        # Configurar jugadores según el modo elegido

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and self.current_player == self.human_player:
                    self.handle_human_turn(event.pos)

            # Si es el turno de la IA
            if self.current_player == self.ai_player and mode == 1:
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

