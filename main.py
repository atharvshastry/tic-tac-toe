from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional #optional
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="Tic Tac Toe by Bhai")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # matlab koi bhi website connect kar sakti hai (local testing ke liye)
    allow_methods=["*"],   # GET, POST, sab allow
    allow_headers=["*"],
)

state = [0,0,0,0,0,0,0,0,0]
turn = 1

class MoveRequest(BaseModel):
    position: int

def checkwin():
    wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    for win in wins:
        if state[win[0]] == state[win[1]] == state[win[2]] !=0:
            return state[win[0]]
    if 0 not in state:
            return 0
    return None

@app.get("/state")
def get_state():
    return {
        "state": state,     
        "turn": turn,        
        "winner": checkwin()
    }

@app.post("/move")
def make_move(move: MoveRequest):
    global turn
    pos = move.position
    if pos < 0 or pos > 8:
        return {"error": "0 se 8 ke beech daal bhai"}
    if state[pos] != 0:
        return {"error": "Ye jagah pehle se bhari hai!"}

    state[pos] = 1 if turn == 1 else -1

    winner = checkwin()

    if winner is None:     
        turn = 1 - turn     

    return {
        "state": state.copy(),
        "turn": turn,
        "winner": winner
    }
@app.post("/reset")
def reset_game():
    global state, turn
    state = [0, 0, 0, 0, 0, 0, 0, 0, 0]   # board saaf
    turn = 1                              # X se shuru
    return {"message": "Naya game shuru ho gaya bhai!"}
@app.get("/")
async def root():
    global state, turn
    state = [0] * 9    # ← har baar nayi game
    turn = 1
    return FileResponse("static/index.html")
app.mount("/", StaticFiles(directory="static", html=True), name="static")