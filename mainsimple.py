# main.py

from board import Board
from player import Player
from ai import AIPlayer


def main():
    # Configuración inicial
    board_size = 19
    board = Board(board_size)

    # Selección del modo de juego
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
    player1 = Player("Jugador 1", "X")
    if mode == 1:
        player2 = AIPlayer("IA", "O")
    else:
        player2 = Player("Jugador 2", "O")

    # Bucle principal del juego
    board.display()
    current_player = player1

    while not board.is_game_over():
        print(f"Turno de {current_player.name} ({current_player.symbol})")

        if isinstance(current_player, Player):  # Turno del jugador humano
            move = current_player.get_move(board)
        else:  # Turno de la IA
            move = current_player.get_best_move(board)

        if board.make_move(move, current_player.symbol):
            board.display()  # Mostrar el tablero después del movimiento

            # Verificar victoria por alineación o captura
            if board.check_winner(current_player.symbol):
                print(f"¡{current_player.name} ha ganado!")
                break

            # Cambiar al siguiente jugador
            current_player = player2 if current_player == player1 else player1
        else:
            print("Movimiento inválido. Inténtalo de nuevo.")

    # Fin del juego
    if board.captures["X"] >= 10:
        print("¡Jugador 1 gana por capturas!")
    elif board.captures["O"] >= 10:
        print("¡Jugador 2 gana por capturas!")
    elif board.is_draw():
        print("¡Es un empate!")
    elif board.acabose != ".":
        print("Gana jugador de " + board.acabose)


if __name__ == "__main__":
    main()


