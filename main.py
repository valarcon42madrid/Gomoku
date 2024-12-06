import subprocess

def main():
    print("Selecciona una opción:")
    print("A: Ejecutar con visualizador gráfico de tablero")
    print("B: Ejecutar versión en terminal (puro python)")
    
    opcion = input("Elige una opción (A/B): ").strip().upper()
    
    if opcion == 'A':
        subprocess.run(["python", "mainvisual.py"])
    elif opcion == 'B':
        subprocess.run(["python", "mainsimple.py"])
    else:
        print("Opción no válida. Por favor, elige A o B.")

if __name__ == "__main__":
    main()
