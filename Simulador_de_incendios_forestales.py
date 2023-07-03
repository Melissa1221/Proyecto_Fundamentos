import random
from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk


def emoji_img(tamaño, texto):
    fuente = ImageFont.truetype("seguiemj.ttf", size=round(tamaño*3/4)) 
    im = Image.new("RGBA", (tamaño, tamaño), (255, 255, 255, 0))
    dibujar = ImageDraw.Draw(im)
    dibujar.text((tamaño/2, tamaño/2), texto, embedded_color=True, font=fuente, anchor="mm")
    return ImageTk.PhotoImage(im)

n = 30
m = 30

ventana = tk.Tk()
ventana.title("Simulación de Bosque")
ventana.geometry("900x900")
canvas = tk.Canvas(ventana, width=m*30, height=n*30)
canvas.pack()


tasa_crecimiento = 0.01

probabilidad_quemarse_vecino = 0.05

tiempo_quemado_necesario = 5

VACIO = '⬜'
ARBOL1 = '🌲'
ARBOL2 = '🌴'
ARBOL3 = '🌳'
FUEGO = '🔥'
LAGO = '🌊'
QUEMADO = '💀'

emoji_arbol1 = emoji_img(30, ARBOL1)
emoji_arbol2 = emoji_img(30,ARBOL2 )
emoji_arbol3 = emoji_img(30, ARBOL3)
emoji_vacio = emoji_img(30, VACIO)
emoji_fuego = emoji_img(30, FUEGO)
emoji_lago = emoji_img(30, LAGO)
emoji_quemado = emoji_img(30, QUEMADO)


probabilidad_quemarse = {
    emoji_arbol1: 0.04,  
    emoji_arbol2: 0.01,  
    emoji_arbol3: 0.02
}

bosque = [[emoji_vacio] * m for _ in range(n)]
tiempo_quemado = [[0] * m for _ in range(n)]



def dibujar_bosque():
    canvas.delete("all") 
    
    for i in range(n):
        for j in range(m):
            x1 = j * 30
            y1 = i * 30
            x2 = x1 + 30
            y2 = y1 + 30
            
            estado = bosque[i][j]
            
            
            canvas.create_image((x1 + x2) // 2, (y1 + y2) // 2, image=estado, anchor="center") 

def obtener_vecinos(i, j):
    vecinos = []
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0 and dy == 0:
                continue
            ni = i + dx
            nj = j + dy
            if 0 <= ni < n and 0 <= nj < m:
                vecinos.append((ni, nj))
    return vecinos

num_lagos = random.randint(20, 40)
for _ in range(num_lagos):
    i = random.randint(0, n - 1)
    j = random.randint(0, m - 1)
    bosque[i][j] = emoji_lago

def SimulaciónTerminada():
    for i in range (n):
        for j in range(m):
            if bosque[i][j]!=emoji_quemado and bosque[i][j] != emoji_lago:
                return False
    return True

def Simulación():
    for i in range(n):
        for j in range(m):
            if bosque[i][j] == emoji_vacio and random.random() < tasa_crecimiento:
                tipo_arbol = random.choice([emoji_arbol1, emoji_arbol2, emoji_arbol3])
                bosque[i][j] = tipo_arbol
    
    for i in range(n):
        for j in range(m):
            if bosque[i][j] in [emoji_arbol1, emoji_arbol2, emoji_arbol3] and random.random() < probabilidad_quemarse[bosque[i][j]]:
                bosque[i][j] = emoji_fuego
                tiempo_quemado[i][j] = 1
            elif bosque[i][j] == emoji_fuego:
                vecinos = obtener_vecinos(i, j)
                for ni, nj in vecinos:
                    if bosque[ni][nj] in [emoji_arbol1, emoji_arbol2, emoji_arbol3] and random.random() < probabilidad_quemarse_vecino:
                        bosque[ni][nj] = emoji_fuego
                        tiempo_quemado[i][j] = 1

    for i in range(n) :
        for j in range (m):
            if bosque[i][j] == emoji_fuego:
                tiempo_quemado[i][j] += 1
                if tiempo_quemado[i][j] >= tiempo_quemado_necesario:
                    bosque[i][j] = emoji_quemado
    dibujar_bosque()
    if SimulaciónTerminada()== True:
        print("Simulación terminada.")
        return
    ventana.after(100, Simulación)  

Simulación()
ventana.mainloop()
