let playerCount = 2; // Jugadores iniciales

// Función para añadir jugadores
function addPlayer() {
    playerCount++;
    const playerDiv = document.createElement("div");
    playerDiv.classList.add("player");
    playerDiv.innerHTML = `
        <span>Jugador ${playerCount}</span>
        <input type="text" placeholder="Ej: Qh Jd">
        <span class="equity">Equity: --%</span>
        <button class="remove-btn" onclick="removePlayer(this)">X</button>
    `;

    document.getElementById("players").appendChild(playerDiv);
}

// Función para eliminar jugadores
function removePlayer(button) {
    button.parentElement.remove();
}

// Función para cambiar de fase
function changePhase(phase) {
    document.querySelectorAll(".menu button").forEach(btn => {
        btn.classList.remove("active");
    });

    document.getElementById(phase).classList.add("active");

    let message = "";
    switch (phase) {
        case "preflop":
            message = "No es necesario añadir más cartas";
            break;
        case "flop":
            message = "Añade 3 cartas al board";
            break;
        case "turn":
            message = "Añade 4 cartas al board";
            break;
        case "river":
            message = "Añade 5 cartas al board";
            break;
    }
    document.getElementById("boardMessage").innerText = message;
}

// Función para calcular equity
function calculate() {
    document.querySelectorAll(".equity").forEach(equity => {
        equity.innerText = "Equity: 50%";
    });
}


