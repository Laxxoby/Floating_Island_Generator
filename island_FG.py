import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from math import sqrt
import random
import svgwrite

"""
    Este programa genera una visualizacion 3d de una isla flotante formada por cubos 3d y crea un archivo .svg 
    que muestra una visualizacion 2d donde enseña el plano superior con los numero de bloques 
    que deben ir en la parte inferior.
"""

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


def main():
    #mapear()
    generar_plataforma()

# Crear un objeto que sea un cubo
class Cubo: 
    def __init__(self, origen): #ejem [0.5, 0.5, 0.5]
        x,y,z = origen[0], origen[1], origen[2]
        self.origen = origen
        self.vertices = np.array([
            [x - 0.5, y - 0.5, z - 0.5], [x + 0.5, y - 0.5, z - 0.5], [x + 0.5, y + 0.5, z - 0.5], [x - 0.5, y + 0.5, z - 0.5],  # Cara de abajo
            [x - 0.5, y - 0.5, z + 0.5], [x + 0.5, y - 0.5, z + 0.5], [x + 0.5, y + 0.5, z + 0.5], [x - 0.5, y + 0.5, z + 0.5]
            ])
        self.caras = [
            [self.vertices[0], self.vertices[1], self.vertices[2], self.vertices[3]],  # Cara de abajo
            [self.vertices[4], self.vertices[5], self.vertices[6], self.vertices[7]],  # Cara de arriba
            [self.vertices[0], self.vertices[1], self.vertices[5], self.vertices[4]],  # Cara lateral
            [self.vertices[2], self.vertices[3], self.vertices[7], self.vertices[6]],  # Cara lateral
            [self.vertices[1], self.vertices[2], self.vertices[6], self.vertices[5]],  # Cara trasera
            [self.vertices[0], self.vertices[3], self.vertices[7], self.vertices[4]]   # Cara delantera
        ]
        

def generar_plataforma():

    """
    Genera una plataforma tridimensional formada por un conjunto de cubos dentro de un círculo.

    Parámetros:
    radio -- Radio del círculo que define la forma de la plataforma.
    altura -- Altura de la plataforma.

    La función crea una plataforma tridimensional dentro de un círculo con el radio dado.
    Los cubos se generan en posiciones dentro del círculo y se apilan en función de la altura,
    creando una estructura visual representativa de una plataforma.
    """
    
    #Función para validar los datos de entrada
    radio, altura, modeIsland = validar_datos()
    
    global ax
    centro_x, centro_y = radio + 1 , radio + 1 # Calcular el centro de la imagen
    ArrAltura = np.zeros(((radio * 2) + 3 , (radio * 2) + 3 ))
    
    for i in range((radio * 2) + 1):
        for j in range((radio * 2) + 1):
            distancia = (i - centro_x)**2 + (j - centro_y)**2  # Calcular la distancia al centro
            
            # Si la distancia es menor o igual al radio al cuadrado, está dentro del círculo
            if distancia <= radio**2 - 1:
                caja1 = Cubo([i + 0.5 , j + 0.5, altura + 0.5])
                cubo = Poly3DCollection(caja1.caras, alpha=0.25, facecolors='green')
                ax.add_collection3d(cubo)
                artura = AlturaIsla(distancia, radio, altura, i, j, modeIsland)    
                ArrAltura[i, j] = artura        
    crear_cuadrados_svg(ArrAltura,radio)
                
    # Establecer los límites de los ejes
    ax.set_xlim([0, (radio * 2) + 1])
    ax.set_ylim([0, (radio * 2) + 1])
    ax.set_zlim([0, altura + 3])

    # Etiquetar los ejes
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Mostrar el gráfico
    #plt.show()

def AlturaIsla(distancia, radio, altura, i, j, modeIsland):
    """
    Calcula la altura de cada cubo en función de su distancia al centro de la isla, y genera la representación gráfica en 3D.

    Parámetros:
    distancia -- Distancia al centro de la isla.
    radio -- Radio del círculo que define la isla.
    altura -- Altura máxima que puede tener la isla.
    i -- Coordenada x del cubo.
    j -- Coordenada y del cubo.

    Retorna:
    Cubos_altura -- Altura del cubo generado.

    La función calcula la altura del cubo dependiendo de la distancia proporcionada y genera un conjunto de cubos en representación gráfica en 3D.
    Además, agrega un texto en la parte superior de algunos cubos mostrando la cantidad de cubos en esa posición.
    """
    global ax 
    porcentaje = ((abs(sqrt(distancia) - radio)) / radio) * 100

    if porcentaje <= 100 and porcentaje > 80:
        Cubos_altura = random.randint(1 if modeIsland == "random" else int(altura * 0.8), altura)
    elif porcentaje <= 80 and porcentaje > 60:
        Cubos_altura = random.randint(1 if modeIsland == "random" else int(altura * 0.6), int(altura * 0.8))
    elif porcentaje <= 60 and porcentaje > 40:
        Cubos_altura = random.randint(1 if modeIsland == "random" else int(altura * 0.4), int(altura * 0.6))
    elif porcentaje <= 40 and porcentaje > 20:
        Cubos_altura = random.randint(1 if modeIsland == "random" else int(altura * 0.2), int(altura * 0.4))
    elif porcentaje <= 20 and porcentaje > 0:
        Cubos_altura = random.randint(1 , int(altura * 0.2))
        # ax.text(i + 0.5, j + 0.5, altura + 1.5, str(Cubos_altura), color='red', fontsize=10, ha='center')

    for z in range(Cubos_altura + 1):
        caja = Cubo([i + 0.5, j + 0.5, (altura - 0.5) - z])
        cubo = Poly3DCollection(caja.caras, alpha=0.25, facecolors='cyan' if z % 2 == 0 else 'blue')
        ax.add_collection3d(cubo)

    return Cubos_altura
    
def crear_cuadrados_svg(ArrAltura, radio = 1):
    filas, columnas = ArrAltura.shape
    lado = 300/(radio) 
    espacio_entre_cuadrillas = lado * 0.1
    dwg = svgwrite.Drawing('Plano2d.svg', profile='full')

    for i in range(filas):
        for j in range(columnas):
            x = j * (lado + espacio_entre_cuadrillas)  # Agregar espacio horizontal entre cuadrillas
            y = i * (lado + espacio_entre_cuadrillas)  # Agregar espacio vertical entre cuadrillas
            numero = int(ArrAltura[i,j])
            dwg.add(dwg.rect(insert=(x, y), size=(lado, lado), fill='#1C2833' if numero == 0  else '#138D75'))
            
            dwg.add(dwg.text((str(numero) if numero > 0 else ""), insert=(x + lado / 2, y + lado / 2), fill='#F4F6F7', font_size=0.3 * lado, text_anchor='middle', alignment_baseline='middle'))

    dwg.save()

def validar_datos():
    print("Bienvenido al generador de islas flotantes de Minecraft")
    radio = validar_numero("Ingresa el radio de la plataforma circular superior: ")
    altura = validar_numero("Ingresa la altura máxima que puede tener la isla flotante: ", 5)
    modo = validar_modo()
    return radio, altura, modo

def validar_numero(mensaje, min_valor=1):
    while True:
        try:
            valor = int(input(mensaje))
            if valor < min_valor:
                print("Por favor, ingresa un número mayor o igual a", min_valor)
                continue
            return valor
        except ValueError:
            print("Por favor, ingresa un número válido.")


def validar_modo():
    while True:
        modo = input("Ingresa el modo en el que se creará la Isla Flotante (random o semiUniforme): ").lower()
        if modo in ["random", "semiuniforme"]:
            return modo
        print("Por favor, ingresa 'random' o 'semiUniforme'.")


if __name__ == '__main__':
    main()