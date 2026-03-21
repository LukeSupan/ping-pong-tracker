# models to pass to the json as dicts

def player_stats():
    return {
        "player": "",
        "wins": 0,
        "losses": 0,
        "games": 0, # redundant but fine. its ping pong
        "winrate": 0.0,
        "pointDiff": 0,
        "pointsEarned": 0,
        "pointsLost": 0,
    }

def matchup_stats():
    return {
        "player1": "",
        "player2": "",
        "games": 0, # redundant but fine. its ping pong
        "player1Wins": 0,
        "player2Wins": 0, # we need both in case of ties
        "pointDiff": 0,
        "player1Points": 0,
        "player2Points": 0,
    }
