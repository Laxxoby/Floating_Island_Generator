import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from math import sqrt
import random
import svgwrite

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


def main():
    #mapear()
    generar_plataforma(5, 10)

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
        

def generar_plataforma(radio, altura):

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
                artura = AlturaIsla(distancia, radio, altura, i, j)    
                ArrAltura[i, j] = artura        
    crear_cuadrados_svg(ArrAltura)
                
    #ax.text(0.5, 0.5, 0.5 + 0.2, "Texto en la cara", color='red', fontsize=12, ha='center')
                
    # Establecer los límites de los ejes
    ax.set_xlim([0, (radio * 2) + 1])
    ax.set_ylim([0, (radio * 2) + 1])
    ax.set_zlim([0, altura + 3])

    # Etiquetar los ejes
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Mostrar el gráfico
    plt.show()

def AlturaIsla(distancia, radio, altura, i, j):
    global ax 
    por = ((abs(sqrt(distancia) - radio) )/ radio ) * 100
    if por <= 100 and por > 80:
        Cubos_altura = random.randint(1, altura)
    if por <= 80 and por > 60:
        Cubos_altura = random.randint(1, int(altura * 0.8))
    if por <= 60 and por > 40:
        Cubos_altura = random.randint(1, int(altura * 0.6))
    if por <= 40 and por > 20:
        Cubos_altura = random.randint(1, int(altura * 0.4))
    if por <= 20 and por > 0:
        Cubos_altura = random.randint(1, int(altura * 0.2))
        ax.text(i + 0.5, j + 0.5, altura + 1.5, str(Cubos_altura), color='red', fontsize=10, ha='center')
    for z in range(Cubos_altura + 1):
        caja = Cubo([i + 0.5 , j + 0.5, (altura - 0.5) - z])
        cubo = Poly3DCollection(caja.caras, alpha=0.25, facecolors='cyan' if z % 2 == 0 else 'blue')
        ax.add_collection3d(cubo)  

    return Cubos_altura
    
def crear_cuadrados_svg(ArrAltura):
    filas, columnas = ArrAltura.shape
    espacio_entre_cuadrillas = 1
    lado = 5
    dwg = svgwrite.Drawing('cuadrados_con_espacio.svg', profile='full')

    for i in range(filas):
        for j in range(columnas):
            x = j * (lado + espacio_entre_cuadrillas)  # Agregar espacio horizontal entre cuadrillas
            y = i * (lado + espacio_entre_cuadrillas)  # Agregar espacio vertical entre cuadrillas
            numero = int(ArrAltura[i,j])
            dwg.add(dwg.rect(insert=(x, y), size=(lado, lado), fill='black' if numero == 0  else 'red'))
            
            dwg.add(dwg.text((str(numero) if numero > 0 else ""), insert=(x + lado / 2, y + lado / 2), fill='white', font_size=3, text_anchor='middle', alignment_baseline='middle'))

    dwg.save()


if __name__ == '__main__':
    main()