from fastapi import FastAPI, HTTPException
from database import init_db, get_db
from models import player_stats, matchup_stats
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# fastAPI please!
app = FastAPI()

# middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# make a model with pydantic


class GameInput(BaseModel):
    player1: str
    player2: str
    score1: int
    score2: int


# make db with tables we need
init_db()

# get games list TODO make sure this is all good, should be
@app.get("/game")
def get_game():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM games")

    rows = cur.fetchall()

    conn.close()

    # return a list of dicts with each row as a dict
    return [dict(row) for row in rows]


# insert game into the table in database (POST)
@app.post("/game")
def add_game(game: GameInput):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("INSERT INTO games (player1, player2, score1, score2) VALUES (?, ?, ?, ?)",
                (game.player1, game.player2, game.score1, game.score2))

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

    # lets us know how many rows were affect, if its none that means nothing was deleted
    if cur.rowcount == 0:
        conn.close()
        raise HTTPException(
            status_code=404, detail=f"game with id {id} not found")

    conn.commit()
    conn.close()

    # if it got deleted successfully
    return {"message": f"deleted game with id: {id}"}

# TODO put endpoint for update
# TODO frontend save button for each row
# TODO(stretch) edit mode to enable or disable edit
# probably would be best to just get it over with and go to css
@app.put("/game/{id}")
def put_game():
    conn = get_db()
    cur = conn.cursor()

    cur.execute()


# calculate and return player_stats (GET)
@app.get("/player-stats")
def get_player_stats():
    conn = get_db()
    cur = conn.cursor()

    # get all the games
    cur.execute("SELECT * FROM games")
    rows = cur.fetchall()

    # use a dict of player_data keyed by player name
    player_data = {}

    # go through each game
    for row in rows:

        # get all info from database for easier manipulation
        player1 = row["player1"]
        player2 = row["player2"]
        score1 = row["score1"]
        score2 = row["score2"]

        if player1 not in player_data:  # if player isnt in the dict already, make player_stats for them
            player_data[player1] = player_stats()
            player_data[player1]["player"] = player1

        if player2 not in player_data:  # if player isnt in the dict already, make player_stats for them
            player_data[player2] = player_stats()
            player_data[player2]["player"] = player2

        # update wins and losses based on score
        # in the case of tie it doesnt increment wins, losses, or games. but also you dont tie in ping pong. im just including the chance so it doesnt directly break this
        # it does screw up winrates and points though
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

        # update pointsEarned and lost
        player_data[player1]["pointsEarned"] += score1
        player_data[player1]["pointsLost"] += score2

        player_data[player2]["pointsLost"] += score1
        player_data[player2]["pointsEarned"] += score2

    # update for stats that dont need to be incremented on a per game basis
    for player in player_data:
        wins = player_data[player]["wins"]
        games = player_data[player]["games"]
        pointsEarned = player_data[player]["pointsEarned"]
        pointsLost = player_data[player]["pointsLost"]

        # update winrate
        player_data[player]["winrate"] = round(
            (wins / games) * 100, 1) if games > 0 else 0

        # update point diff
        player_data[player]["pointDiff"] = pointsEarned - pointsLost

    # close the connection
    conn.close()

    # return the list of the values, itll be packaged as a json
    return list(player_data.values())

# calculate and return matchup_stats (GET)


@app.get("/matchup-stats")
def get_matchup_stats():
    conn = get_db()
    cur = conn.cursor()

    # select the games
    cur.execute("SELECT * FROM games")

    # get rows from db
    rows = cur.fetchall()

    # dict of matchups keyed by a matchup tuple
    matchup_data = {}

    for row in rows:

        # sort tuple to always have the same matchup. then update the matchup key
        matchup_key = tuple(sorted([row["player1"], row["player2"]]))

        # save the players in correct order
        player1 = matchup_key[0]
        player2 = matchup_key[1]

        # save scores properly (not sure the best way to do this but this works)
        swapped = row["player1"] != player1
        score1 = row["score2"] if swapped else row["score1"]
        score2 = row["score1"] if swapped else row["score2"]

        # add key to matchup_data if this matchup hasnt occured before
        if matchup_key not in matchup_data:
            matchup_data[matchup_key] = matchup_stats()
            matchup_data[matchup_key]["player1"] = player1
            matchup_data[matchup_key]["player2"] = player2

        # update values (games, player1wins, player2wins, pointDiff after, player1points, player2points)

        # update wins and losses based on score
        # in the case of tie it doesnt increment wins, losses, or games. but also you dont tie in ping pong. im just including the chance so it doesnt directly break this
        # it does screw up winrates and points though
        # just dont do ties. unless you really want to i guess.
        if score1 > score2:
            matchup_data[matchup_key]["player1Wins"] += 1
            matchup_data[matchup_key]["games"] += 1

        elif score2 > score1:
            matchup_data[matchup_key]["player2Wins"] += 1
            matchup_data[matchup_key]["games"] += 1

        # update total score
        matchup_data[matchup_key]["player1Points"] += score1
        matchup_data[matchup_key]["player2Points"] += score2

    # point diff calculation at the end, more efficient
    for matchup in matchup_data:
        matchup_data[matchup]["pointDiff"] = matchup_data[matchup]["player1Points"] - \
            matchup_data[matchup]["player2Points"]

    # close the connection
    conn.close()

    # return the matchup_data
    return list(matchup_data.values())
