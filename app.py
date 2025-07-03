from flask import Flask, render_template, request
import time, threading
from userlock import is_authorized

app = Flask(__name__)
running = False

@app.route('/', methods=['GET', 'POST'])
def index():
    global running
    status = "Waiting..."
    if request.method == 'POST':
        token = request.form.get('token')
        convo_id = request.form.get('convo_id')
        hater_name = request.form.get('hater_name')
        speed = request.form.get('speed')
        stop_key = request.form.get('stop_key')
        upi = request.form.get('upi')
        password = request.form.get('password')
        file = request.files['message_file']

        if not is_authorized(upi, password):
            status = "❌ Access Denied: Invalid UPI or Password"
            return render_template('index.html', status=status)

        messages = file.read().decode().splitlines()
        running = True

        def send():
            for msg in messages:
                if not running:
                    break
                print(f"[{hater_name}] {convo_id} => {msg}")
                time.sleep(int(speed))

        threading.Thread(target=send).start()
        status = "🚀 Loader Started"

    return render_template('index.html', status=status)

@app.route('/stop', methods=['POST'])
def stop():
    global running
    running = False
    return "🛑 Loader Stopped"

if __name__ == '__main__':
    app.run(debug=True)
