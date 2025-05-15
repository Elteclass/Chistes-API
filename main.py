from machine import Pin, I2C
import ssd1306
import time
import random

# Inicialización del OLED
i2c = I2C(0, scl=Pin(1), sda=Pin(0))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Lista de chistes simulando una API
chistes = [
    "¿Qué hace una abeja en el gimnasio? ¡Zum ba!",
    "¿Por qué lloraba el libro de matemáticas? ¡Porque tenía muchos problemas!",
    "¿Cómo se llama un león con dos cabezas? ¡Un león-león!",
    "¿Qué le dijo una impresora a otra? ¿Esa hoja es tuya o es una impresión mía?",
    "¿Por qué el tomate se sonrojó? Porque vio la ensalada desnuda.",
    "¿Qué hace un pez? ¡Nada!",
    "¿Cuál es el colmo de Aladdín? Tener mal genio.",
    "¿Por qué los pájaros no usan Facebook? ¡Porque ya tienen Twitter!",
    "¿Qué hace un perro con un taladro? ¡Taladrando!",
    "¿Cuál es el café más peligroso del mundo? El ex-preso."
]

# Función para mostrar texto en múltiples líneas
def mostrar_chiste(chiste):
    oled.fill(0)
    oled.text("Obteniendo...", 0, 0)
    oled.show()
    time.sleep(1)

    oled.fill(0)
    oled.text("Chiste:", 0, 0)

    palabras = chiste.split()
    linea = ""
    lineas = []

    for palabra in palabras:
        if len(linea + palabra) < 20:
            linea += palabra + " "
        else:
            lineas.append(linea)
            linea = palabra + " "
    lineas.append(linea)

    for i, l in enumerate(lineas[:5]):
        oled.text(l.strip(), 0, 10 + i * 10)

    oled.show()

# Bucle principal: cambiar chiste cada 5 segundos
while True:
    chiste = random.choice(chistes)
    mostrar_chiste(chiste)
    time.sleep(5)
