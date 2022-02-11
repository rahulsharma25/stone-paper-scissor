from flask import Flask, Response, url_for, render_template
from camera import Camera
import cv2 as cv

app = Flask(__name__)
cam = Camera(0.8)

@app.route("/")
def home():
    return render_template('index.html')

def gen_frames():
    while True:
        frame = cam.get_frame()

        ret, buffer = cv.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/stream")
def stream():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)