import socketio
sio = socketio.Client(engineio_logger=True)
start_timer = None

if __name__ == '__main__':
   sio.connect('http://127.0.0.1:3000')
   sio.emit('connected', {"Data": "Device_id"})
   sio.wait()

