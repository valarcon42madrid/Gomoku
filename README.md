PRE:

python -m venv mi_entorno 

.\mi_entorno\Scripts\Activate 

pip install pygame


PLAY:

python main.py

 
NOTAS:

He agilizado el primer movimiento de la AI ya que el minmax era un error (ponía en la esquina perjudicando su posición; ahora pone a una distancia de dos de la ficha enemiga)

El ultimo cambio arregla el error de que si puedes capturar 5 alineadas pero capturas en otro lugar, aún continúa la partida.
Ahora en caso de doble victoria gana el primer jugador ganador.
