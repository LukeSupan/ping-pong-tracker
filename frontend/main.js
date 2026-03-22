const { createElement } = require("react");

/*
 * DOM references
 */
const submitButton = document.getElementById("submit-game");

/*
 * main functionality
 */
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
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      player1: player1Box.value.trim(),
      player2: player2Box.value.trim(),
      score1: parseInt(score1Box.value),
      score2: parseInt(score2Box.value),
    }),
  });

  // reset inputs
  player1Box.value = "";
  player2Box.value = "";
  score1Box.value = "";
  score2Box.value = "";

  // call displaying stats function
  updateCards();
}

/*
 * display functions
 */
// games section display
async function displayGames() {
  const gamesWrapper = document.getElementById("games-wrapper");

  const response = await fetch("http://127.0.0.1:8000/games");

  const data = await response.json();

  // loop through data, make an element for each in the wrapper, make a delete button, give it a listener to delete the game with this id
  data.forEach((game, index) => {
    
    const gameRow = createElement("div");
    
    // make a row of the info with a text box for each so they can be edited later maybe? more now set as readonly
    // then a delete button at the end

  });
}

// player card section display
async function displayPlayers() {
  const playerStatsWrapper = document.getElementById("player-stats-wrapper");

  const response = await fetch("http://127.0.0.1:8000/player-stats");

  const data = await response.json();

  playerStatsWrapper.innerHTML = "";

  // each player is formatted
  data.forEach((player, index) => {
    const card = document.createElement("div");
    card.id = `player-card-${index}`;

    // simple plugin, but if pointDiff is negative dont add a plus. yay.
    card.innerHTML = `
            <p><span>${player.player}</span> <span class="winrate">${player.winrate}%</span></p>
            <p>${player.wins} W / ${player.losses} L</p>
            <p>Points Earned: ${player.pointsEarned}</p>
            <p>Points Lost: ${player.pointsLost}</p>
            <p><span class="point-diff">Point Differential: ${player.pointDiff >= 0 ? "+" : ""} ${player.pointDiff}</span></p>
        `;

    playerStatsWrapper.appendChild(card);
  });

  console.log(data);
}

// matchup card section display
async function displayMatchups() {
  const matchupStatsWrapper = document.getElementById("matchup-stats-wrapper");

  const response = await fetch("http://127.0.0.1:8000/matchup-stats");

  const data = await response.json();

  matchupStatsWrapper.innerHTML = "";

  data.forEach((matchup, index) => {
    const card = document.createElement("div");
    card.id = `matchup-card-${index}`;

    // simple plugin, but if pointDiff is negative dont add a plus. yay.
    card.innerHTML = `
            <p>${matchup.player1} vs ${matchup.player2} - ${matchup.games} Games</p>
            <p>Wins: ${matchup.player1Wins} W | ${matchup.player2Wins} W</p>
            <p>Points: ${matchup.player1Points} | ${matchup.player2Points} </p>
            <p>Point Differential: ${matchup.pointDiff >= 0 ? "+" : ""} ${matchup.pointDiff}</p>
        `;

    matchupStatsWrapper.appendChild(card);
  });

  console.log(data);
}

/*
 * helper functions
 */
function updateCards() {
  displayPlayers();
  displayMatchups();
}

/*
 * init
 */
updateCards();

/*
 * event listeners
 */
submitButton.addEventListener("click", submitGame);
