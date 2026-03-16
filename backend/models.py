# models to pass to the json as dicts

# each game has a model
def game():
    return {
        "player1": "",
        "player2": "",
        "score1": 0,
        "score2": 0, 
    }

def player_stats():
    return {
        "player": "",
        "wins": 0,
        "losses": 0,
        "games": 0, # redundant but fine. its ping pong
        "pointdiff": 0.0,
    }

def matchup_stats():
    return {
        "player1": "",
        "player2": "",
        "games": 0,
        "player1wins": 0,
        "pointdiff": 0.0,
    }

