# ============================================================================
# Nombre del estudiante: Jaime Antonio Alvarez Crisóstomo
# Materia: Lenguajes de Interfaz
# Título del proyecto: Obtención de chistes desde una API (deepseek) en pantalla OLED
# Fecha: 15/05/2025
#
# Descripción:
# Este programa realiza la conexión a una API externa para obtener chistes de forma aleatoria.
# ============================================================================

from machine import I2C, Pin
import ssd1306
import network
import urequests
import time
import json

# --- Configuración WiFi ---
WIFI_SSID = "TecNM-ITT"
WIFI_PASSWORD = ""

# --- Configuración API ---
API_URL = "https://api.deepseek.com/v1/chat/completions"  # Ejemplo con DeepSeek
API_KEY = "MIAPIKEY"  # Reemplaza con tu clave real
API_HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# --- Configuración OLED ---
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400_000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# --- Función para conectar WiFi ---
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Conectando a WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
    print("¡Conectado! IP:", wlan.ifconfig()[0])

# --- Función para obtener chiste de la API ---
def get_joke():
    try:
        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": "Dime un chiste corto y divertido"}]
        }
        response = urequests.post(API_URL, headers=API_HEADERS, json=data)
        joke = response.json()["choices"][0]["message"]["content"]
        response.close()
        return joke
    except Exception as e:
        print("Error en API:", e)
        return "Error al conectar con la API"

# --- Función para mostrar texto en OLED ---
def show_text(text):
    oled.fill(0)
    lines = []
    # Divide el texto en líneas de 16 caracteres
    while text:
        space_pos = text[:16].rfind(' ')
        cut = 16 if space_pos == -1 else space_pos + 1
        lines.append(text[:cut])
        text = text[cut:]
    # Muestra hasta 4 líneas
    for i, line in enumerate(lines[:4]):
        oled.text(line, 0, i * 16)
    oled.show()

# --- Programa principal ---
def main():
    connect_wifi()
    while True:
        joke = get_joke()
        print("Chiste recibido:", joke)
        show_text(joke)
        time.sleep(30)  # Espera 30 segundos entre chistes

if __name__ == "__main__":
    main()
