from fastapi import FastAPI
from database import init_db, get_db
from models import player_stats, matchup_stats, game
from pydantic import BaseModel

app = FastAPI()

# make a model with pydantic
class GameInput(BaseModel):
    player1: str
    player2: str
    score1: int
    score2: int

# make db with tables we need
init_db()


# insert game into the table in database (POST)
@app.post("/game")
def add_game(game: GameInput):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("INSERT INTO games (player1, player2, score1, score2) VALUES (?, ?, ?, ?)", (game.player1, game.player2, game.score1, game.score2))

    # commit changes and close the connection
    conn.commit()
    conn.close()

    return {"message": "inserted a game!"}

# delete game "id" from table in database (DELETE)
@app.delete("/game/{id}")
def delete_game(id: int):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM games WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    # f-string for variable
    return {"message": f"deleted game with id: {id}"}

# calculate and return player_stats (GET)
@app.get("/player-stats")
def get_player_stats():
    conn = get_db()
    cur = conn.cursor()

    # get all the games
    cur.execute("SELECT * FROM games")
    rows = cur.fetchall

    player_stats_list = []
    
    # def player_stats():
    #     return {
    #         "player": "",
    #         "wins": 0,
    #         "losses": 0,
    #         "games": 0, # redundant but fine. its ping pong
    #         "winrate": 0.0,
    #         "pointDiff": 0.0,
    #         "pointsEarned": 0,
    #         "pointsLost": 0,
    #     }

    # use a dict of player_data keyed by player name
    player_data = {}
    for row in rows: # each game

        # get all info from database for easier manipulation
        player1 = row["player1"]
        player2 = row["player2"]
        score1 = row["score1"]
        score2 = row["score2"]

        if player1 not in player_data: # if player isnt in the dict already, make player_stats for them
            player_data[player1] = player_stats()
            player_data[player1]["player"] = player1

        if player2 not in player_data: # if player isnt in the dict already, make player_stats for them
            player_data[player2] = player_stats()
            player_data[player2]["player"] = player2

        # TODO YOU WERE GONNA MAKE WINS AND GAMES A VARIABLE FOR EASE OF USE AGAIN. ROCKET LEAGUE


        # update wins and losses based on score
        # in the case of tie it doesnt increment wins or losses, but also you dont tie in ping pong. im just including the chance so it doesnt directly break this
        # it does screw up winrates though if you always increment games, so i got rid of them.
        # just dont do ties. unless you really want to i guess.
        if score1 > score2:
            player_data[player1]["wins"] += 1
            player_data[player2]["losses"] += 1

            player_data[player1]["games"] += 1
            player_data[player2]["games"] += 1

        elif score2 > score1:
            player_data[player2]["wins"] += 1
            player_data[player1]["losses"] += 1
            
            player_data[player1]["games"] += 1
            player_data[player2]["games"] += 1


        # update winrate
        player_data[player1]["winrate"] = round((player_data[player1]["wins"] / player_data[player1]["games"]) * 100, 1) if player_data[player1]["games"] > 0 else 0

        # update pointsEarned and lost

        # update point diff



        player_data[player1]["pointsEarned"] += score1
        player_data[player1]["pointsLost"] += score2




            # also update the matchup, but we are less worried about that for now


            
    # return the list of the values, itll be packaged as a json
    return list(player_data.values())

# calculate and return matchup_stats (GET)
@app.get("matchup-stats")
def get_matchup_stats():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
                CREATE TABLE IF NOT EXISTS games (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player1 TEXT,
                    player2 TEXT,
                    score1 INTEGER,
                    score2 INTEGER
                )
    """)



    return {"message": "hello"}
