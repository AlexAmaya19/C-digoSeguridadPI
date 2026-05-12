

# Sistema de Seguridad con Detección de Intrusos (YOLOv8 + Raspberry Pi)

Este proyecto consiste en un sistema de vigilancia inteligente capaz de detectar personas en tiempo real utilizando el modelo **YOLOv8**. Al confirmar la presencia de un intruso, el sistema activa una alarma visual y sonora mediante hardware (LEDs y Buzzer) y guarda una evidencia fotográfica.

## 🚀 Características

* **IA de Vanguardia:** Utiliza YOLOv8n para una detección rápida y precisa.
* **Filtro de Falsos Positivos:** Requiere 3 detecciones consecutivas para activar la alarma.
* **Control de Hardware:** Interfaz directa con GPIO para activar ráfagas de luces y sonido.
* **Optimización de Almacenamiento:** Captura y sobreescribe la imagen de evidencia cada 5 detecciones para no saturar el disco.
* **Cero Lag:** Implementa limpieza de buffer de cámara para procesamiento en tiempo real.

## 🛠️ Requisitos de Hardware

* Raspberry Pi (Zero 2W, 3B, 4 o 5).
* Cámara Web USB o Módulo de Cámara compatible.
* 2 LEDs (Conectados a los pines GPIO 17 y 22).
* 1 Buzzer Activo (Conectado al pin GPIO 27).
* Resistencias y cables de conexión.

## 📦 Instalación y Configuración

1. **Clonar el repositorio:**
```bash
git clone https://github.com/[TuUsuario]/[TuRepositorio].git
cd [PIA_YOLO_Seguridad ]

```


2. **Crear y activar entorno virtual (Recomendado):**
```bash
python -m venv env
source env/bin/activate

```


3. **Instalar dependencias:**

```bash
   pip install -r requirements.txt

```

## 🖥️ Uso

Para iniciar el sistema de seguridad, ejecuta:

```bash
python seguridad.py

```

*El sistema cargará el modelo y comenzará el escaneo perimetral automáticamente.*

## 📋 Especificaciones Técnicas (Versiones)

Este proyecto fue desarrollado y probado con las siguientes versiones:

* **YOLOv8:** [8.4.46]
* **PyTorch:** [ 2.0.1]
* **OpenCV:** [4.13.0]

## 📂 Estructura del Proyecto

* `seguridad.py`: Script principal del sistema.
* `yolov8n.pt`: Pesos del modelo pre-entrenado.
* `captura_intruso.jpg`: Archivo donde se guarda la evidencia actualizada.
* `requirements.txt`: Lista de librerías necesarias.

---

### Notas adicionales para tu entrega:

1. Crea un archivo nuevo en GitHub llamado `README.md`.
2. Pega este contenido.
3. No olvides subir también tu archivo `requirements.txt` (recuerda que se genera con `pip freeze > requirements.txt` desde tu Raspberry).

```

```
