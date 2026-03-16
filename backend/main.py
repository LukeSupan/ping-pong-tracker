from fastapi import FastAPI
from database import init_db

app = FastAPI()

# make db with tables we need
init_db()


# insert game into the table in database (POST)
@app.post("/game")
def add_game():
    return {"message": "hello"}

# delete game "id" from table in database (DELETE)
@app.delete("/game/{id}")
def delete_game():
    return {"message": "hello"}

# calculate and return player_stats (GET)
@app.get("/player-stats")
def get_player_stats():
    return {"message": "hello"}

# calculate and return matchup_stats (GET)
@app.get("matchup-stats")
def get_matchup_stats():
    return {"message": "hello"}

# just a test
@app.get("/")
def read_root():
    return {"message": "hello"}

