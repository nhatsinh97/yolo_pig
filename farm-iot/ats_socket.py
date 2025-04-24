# ats_socket.py
import json
import paho.mqtt.client as mqtt
from threading import Thread
from application.controllers.ats_logger import log_ats_data


# Khởi tạo biến socketio, sẽ được truyền từ file chính (app.py)
socketio = None

# Cấu hình MQTT
MQTT_BROKER = "localhost"  # hoặc IP như "10.50.41.15"
MQTT_PORT = 1883
MQTT_TOPIC = "ats/data"

# Hàm callback khi nhận dữ liệu từ MQTT
def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode('utf-8')
        data = json.loads(payload)
        print("[ATS MQTT] Dữ liệu nhận được:", data)

        # 🔴 Ghi dữ liệu vào InfluxDB
        log_ats_data(data)

        # Gửi dữ liệu đến client qua Socket.IO
        if socketio:
            socketio.emit('ats_data', data)

    except Exception as e:
        print("[ATS MQTT] Lỗi:", e)


def start_ats_socketio_listener(socketio_instance):
    global socketio, mqtt_client
    socketio = socketio_instance

    mqtt_client = mqtt.Client()
    mqtt_client.on_message = on_message
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
    mqtt_client.subscribe(MQTT_TOPIC)

    thread = Thread(target=mqtt_client.loop_forever)
    thread.daemon = True
    thread.start()
