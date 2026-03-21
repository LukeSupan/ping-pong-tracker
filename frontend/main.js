// listen for submit button click
const submitButton = document.getElementById("submit-game");

async function submitGame(event) {

    // prevent default
    event.preventDefault()

    // player inputs
    const player1Box = document.getElementById("player1");
    const player2Box = document.getElementById("player2");

    // score inputs
    const score1Box = document.getElementById("score1");
    const score2Box = document.getElementById("score2");

    // post the game with the current values of the box
    const response = await fetch("http://127.0.0.1:8000/game", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ 
            player1: player1Box.value, 
            player2: player2Box.value, 
            score1: parseInt(score1Box.value), 
            score2: parseInt(score2Box.value)
        }),
    })

    const data = await response.json()
    console.log(data)


}

// event listeners
submitButton.addEventListener("click", submitGame)



    // get values from the DOM (player1, player2, score1, score2)

    // send them to the backend via fetch (POST /game)

    // after success, refresh the stats displayed on the page