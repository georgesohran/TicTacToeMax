from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from game import *

app = FastAPI()
game_manager = GameManeger()



@app.post('/game')
def create_game(game_params: GameParams):
  id = game_manager.create_game(game_params)
  return {'detail': 'success', 'game':game_manager.active_games[id]}


@app.websocket('game/{room_id}/{client_id}')
async def ws(websocket: WebSocket, room_id:str, client_id:str):
  await game_manager.active_games[room_id].connect(websocket)
  try:
    while True:
      data = await websocket.receive_json()
      game_manager.active_games[room_id].game_field = data['game_field']
      await websocket.send({'detail':'continue', 'game_field':data['game_field']})
  except WebSocketDisconnect:
     game_manager.active_games[room_id].disconnect(websocket)