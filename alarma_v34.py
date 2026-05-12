import cv2
from ultralytics import YOLO
import time
from gpiozero import LED, Buzzer 

# --- CONFIGURACIÓN ---
MODELO_PATH = "yolov8n.pt"
CLASE_ID = 0
UMBRAL = 0.30
NOMBRE_ARCHIVO_UNICO = "captura_intruso.jpg" # Sobreescritura constante

# --- CONFIGURACIÓN DE HARDWARE ---
led_1 = LED(17)        
led_2 = LED(22)        
buzzer_alarma = Buzzer(27) 

def conectar_camara():
    for puerto in range(4):
        cap = cv2.VideoCapture(puerto, cv2.CAP_V4L2)
        if cap.isOpened():
            success, _ = cap.read()
            if success:
                print(f"✅ Cámara detectada en puerto {puerto}")
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
                cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                return cap
            cap.release()
    return None

print("🧠 Cargando YOLOv8...")
model = YOLO(MODELO_PATH)
cap = conectar_camara()

if cap is None:
    print("🚨 ERROR: No se encontró la cámara.")
    exit()

print("\n🛡️ SISTEMA ARMADO")

contador_detecciones = 0 

try:
    while True:
        # Limpieza de buffer para imagen en tiempo real
        for _ in range(2): cap.read()
        success, frame = cap.read()

        if not success:
            continue

        hora = time.strftime('%H:%M:%S')
        results = model.predict(source=frame, conf=UMBRAL, classes=[CLASE_ID], max_det=3, imgsz=320, verbose=False)

        intruso_encontrado = False
        conf_actual = 0
        
        for r in results:
            for box in r.boxes:
                intruso_encontrado = True
                conf_actual = float(box.conf[0])
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                # --- DIBUJO DE EVIDENCIA (ESTILO v30) ---
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
                texto = f"INTRUSO {conf_actual*100:.1f}%"
                cv2.rectangle(frame, (x1, y1 - 30), (x1 + 220, y1), (0, 255, 0), -1)
                cv2.putText(frame, texto, (x1 + 5, y1 - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

        if intruso_encontrado:
            contador_detecciones += 1
            
            if contador_detecciones >= 3:
                # 1. Sobreescribir foto cada 5 detecciones
                if contador_detecciones % 5 == 0:
                    cv2.imwrite(NOMBRE_ARCHIVO_UNICO, frame)
                    print(f"📸 Evidencia actualizada: {NOMBRE_ARCHIVO_UNICO}")

                # 2. Secuencia de 4 Ráfagas de Alarma
                print(f"[{hora}] 🚨 ¡ALARMA ACTIVA! ({conf_actual*100:.1f}%)")
                
                # Ráfaga 1
                led_1.on(); led_2.off(); buzzer_alarma.on()
                time.sleep(0.08); buzzer_alarma.off(); time.sleep(0.05)
                
                # Ráfaga 2
                led_1.off(); led_2.on(); buzzer_alarma.on()
                time.sleep(0.08); buzzer_alarma.off(); time.sleep(0.05)

                # Ráfaga 3
                led_1.on(); led_2.off(); buzzer_alarma.on()
                time.sleep(0.08); buzzer_alarma.off(); time.sleep(0.05)
                
                # Ráfaga 4
                led_1.off(); led_2.on(); buzzer_alarma.on()
                time.sleep(0.08); buzzer_alarma.off(); time.sleep(0.05)

            else:
                print(f"[{hora}] ⚠️ Verificando... ({contador_detecciones}/3)")
        
        else:
            if contador_detecciones > 0:
                print(f"[{hora}] ✅ Despejado. Apagando periféricos.")
            
            contador_detecciones = 0
            led_1.off(); led_2.off(); buzzer_alarma.off()

except KeyboardInterrupt:
    print("\n🛑 Vigilancia detenida por usuario.")
finally:
    # Limpieza final de pines y cámara
    led_1.off(); led_2.off(); buzzer_alarma.off()
    cap.release()
    cv2.destroyAllWindows()
