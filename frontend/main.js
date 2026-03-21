// listen for submit button click
const submitButton = document.getElementById("submit-game");

updateCards();

// function to submitGame
async function submitGame(event) {

    event.preventDefault();


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
    });

    const data = await response.json();
    console.log(data);

    // reset inputs
    player1Box.value = "";
    player2Box.value = "";
    score1Box.value = "";
    score2Box.value = "";


    // call displaying stats function
    displayPlayers();

}

// function to display players
async function displayPlayers() {
    const playerStatsWrapper = document.getElementById("player-stats-wrapper");

    const response = await fetch("http://127.0.0.1:8000/player-stats");

    const data = await response.json();

    playerStatsWrapper.innerHTML = ""

    // each player is formatted
    data.forEach((player, index) => {
        const card = document.createElement("div");
        card.id = `player-card-${index}`

        // simple plugin, but if pointDiff is negative dont add a plus. yay.
        card.innerHTML= `
            <p><span>${player.player}</span> <span class="winrate">${player.winrate}%</span></p>
            <p>${player.wins} W / ${player.losses} L</p>
            <p>${player.pointsEarned} Points Earned</p>
            <p>${player.pointsLost} Points Lost</p>
            <p><span class="point-diff">${player.pointDiff >= 0 ? "+" : ""}${player.pointDiff}</span> Point Differential</p>
        `

        playerStatsWrapper.appendChild(card);

    });

    console.log(data);
}

// updateCards
function updateCards() {
    displayPlayers();
}

// event listeners
submitButton.addEventListener("click", submitGame)



    // get values from the DOM (player1, player2, score1, score2)

    // send them to the backend via fetch (POST /game)

    // after success, refresh the stats displayed on the page