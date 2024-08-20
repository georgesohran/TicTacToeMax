from fastapi import WebSocket, WebSocketDisconnect
from pydantic import BaseModel
import random
import string


class GameParams(BaseModel):
  name: str | None
  max_players: int
  hight: int
  width: int
  signs2win: int


class GameField:
  def __init__(self, game_params: GameParams):
    self.fields = [[''] * game_params.width] * game_params.heigth
  
  def mark(self, x: int, y: int, sign: str):
    self.fields[x][y] = sign
  
  def serialize(self):
    return self.fields



class GameRoom:
  def __init__(self, game_params: GameParams):
    self.players: list[WebSocket] = []
    self.max_players: int = game_params.max_players
    self.game_field: GameField = GameField(game_params)

  async def connect(self, websocket: WebSocket):
    await websocket.accept()
    if len(self.players) <= self.max_players:
      self.players.append(websocket)
  
  async def disconnect(self, websocket: WebSocket):
    self.players.remove(websocket)

  async def send_game_data(self):
    for player in self.players:
      await player.send_json(self.game_field.serialize()) 



class GameManeger:
  def __init__(self):
    self.active_games: dict[int, GameRoom] = {}
  
  def create_game(self, game_params: GameParams):
    game = GameRoom(game_params)
    if game_params.name:
      self.active_games[game_params.name] = game
    else:
      name = random.choice(string.ascii_letters) * random.randint(3, 10)
      while self.active_games[name]:
        name = random.choice(string.ascii_letters) * random.randint(3, 10)
      self.active_games[name] = game

    return len(self.active_games) + 1
  
