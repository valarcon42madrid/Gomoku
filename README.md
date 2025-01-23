PRE:

python -m venv mi_entorno 

.\mi_entorno\Scripts\Activate 

pip install pygame


PLAY:

python main.py

 
NOTAS:

He agilizado el primer movimiento de la AI ya que el minmax era un error (ponía en la esquina perjudicando su posición; ahora pone a una distancia de dos de la ficha enemiga) y he dejado que cuando te han ganado irremediablemente por alineación de 5 te deje verlo (es decir, espera a que pongas en cualquier lado para decirte que has perdido; esto tambien es debido a que sino te estaría delatando cuando puedes evitar perder capturando la alineación de 5).
