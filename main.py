import time
import logging
from flask import Flask, render_template, Response
import paho.mqtt.client as mqtt

class MqttStreamer:
    def __init__(self):
        self.client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
        self.client.username_pw_set(username="fly", password="123456")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
        self.current_frame = None
        self.last_update_time = 0

    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            print("Connected to MQTT Broker!")
            client.subscribe("/below_cam/img_compress")
        else:
            print(f"Failed to connect, return code {reason_code}")

    def on_message(self, client, userdata, msg):
        if msg.payload:
            self.current_frame = msg.payload
            self.last_update_time = time.time()

    def start(self):
        self.client.connect("118.31.104.242", 1883, 60)
        self.client.loop_start()

    def get_frame(self):
        return self.current_frame

streamer = MqttStreamer()
app = Flask(__name__)

def gen_frames():
    """视频流生成器"""
    while True:
        frame = streamer.get_frame()
        if frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(1)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    streamer.start()
    app.run(host="0.0.0.0", port=5500, debug=False)