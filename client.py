import json

import socketio
import board
sio = socketio.Client(engineio_logger=True)
start_timer = None
#To pass the client id
partie = board.nouvelle_partie("1")

@sio.on('server response')
def handle_json(data):
    print('received data from broadcast: ' + data)
    print("TYPE OF RECEIVED DATA = ", type(data))
    update_move = json.loads(data)

    #If the other client has sent the data, update the move and refresh screen
    # sid will not be equal if the other client has sent it
    print("sio.sid",sio.sid)
    print("update_move[sid]", update_move["sid"])
    #Update move -> if the other client has sent it. ie, sid will not be equal
    if update_move["sid"] != sio.sid:
       partie.make_auto_move(update_move["move"])

if __name__ == '__main__':
    sio.connect('http://127.0.0.1:3000')
    print(sio.sid,"connected to server")
    while True:
        partie.jouer("Noir")
        print("played ")
        if partie.make_move:
            print("move made !!! ")
            data = partie.last_move + partie.move_coord
            sid_client = sio.sid
            print("SENDING SID ", sid_client)
            x = {"sid": sid_client, "move": str(data)}
            x_json = json.dumps(x)
            sio.emit('connected', x_json)


    # while True:
    #
    #       if partie.make_move:
    #
    #          partie.make_move = False
    #          sio.emit('connected', partie.last_move)
    #       else:
    #           sio.wait()


