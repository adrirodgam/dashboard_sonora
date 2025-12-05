# Sonora IoT Climate Dashboard

Proyecto de monitoreo climático desarrollado con Django, MQTT y Python.
Permite recibir datos desde sensores IoT, almacenarlos en base de datos, graficarlos en tiempo real y consultar historial por municipio.

## Características del sistema
- Recepción de mediciones mediante MQTT (topic: `sonora/#`)
- Visualización en dashboard web con Django
- Gráficas dinámicas para temperatura, humedad y luz
- Historial almacenado en SQLite con exportación CSV
- Sistema de alertas por condiciones extremas
- Simulador de datos para pruebas sin hardware

## Tecnologías
| Tecnología | Uso |
|---|---|
| Django 6.x | Backend y dashboard web |
| MQTT + Paho-MQTT | Comunicación IoT |
| SQLite3 | Base de datos local |
| Chart.js | Visualización de datos |
| Python 3.12–3.13 | Entorno recomendado |

## Instalación
1. Clonar el repositorio:
git clone https://github.com/usuario/dashboard_sonora.git
cd dashboard_sonora

2. Crear entorno virtual (Python 3.12 o 3.13)
python -m venv venv
venv/Scripts/activate

3. Instalar dependencias
pip install "Django>=6.0,<7.0"
pip install paho-mqtt==1.6.1

## Ejecución del proyecto
### Terminal 1 – Servidor Django
venv/Scripts/activate
python manage.py migrate
python manage.py runserver

Acceso web: http://127.0.0.1:8000/

### Terminal 2 – Cliente MQTT
venv/Scripts/activate
python -m dashboard.mqtt_client

Simulador opcional:
python simulador_mqtt.py

## Estructura
dashboard_sonora/
 ├─ dashboard/
 ├─ monitoreo/
 ├─ manage.py
 ├─ db.sqlite3
 ├─ mqtt_client.py
 └─ simulador_mqtt.py

## Consideraciones
- Python 3.14 no es compatible. Usar 3.13 o 3.12.
- El broker MQTT transmite en tiempo real, no conserva histórico.
- SQLite mantiene los datos incluso si el servidor se apaga.

## Autor
Adriana Rodríguez
Proyecto Final IoT — Sonora, 2025
