import socketio
import board
sio = socketio.Client(engineio_logger=True)
start_timer = None

if __name__ == '__main__':
    partie = board.nouvelle_partie()
    sio.connect('http://127.0.0.1:3000')
    while True:
          partie.jouer()
          current_state = json. dumps(partie.pieces)
          sio.emit('connected', current_state)
    sio.wait()
