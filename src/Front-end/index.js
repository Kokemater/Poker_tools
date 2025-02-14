let playerCount = 2; // Jugadores iniciales

// Función para añadir jugadores
function addPlayer() {
    playerCount++;
    const playerDiv = document.createElement("div");
    playerDiv.classList.add("player");
    playerDiv.innerHTML = `
        <div class="player-wrapper">
			<span>Jugador ${playerCount}</span>
			<input type="text" placeholder="Ej: Qh Jd">
			<span class="equity">Equity: --%</span>
		</div>
		<button class="remove-btn" onclick="removePlayer(this)">:(</button>
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
    const players = [];
    document.querySelectorAll(".player input").forEach(input => {
        players.push(input.value.trim());
    });

    const data = { players };

    fetch("http://127.0.0.1:8000/api/calculate/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        const equities = result.equities;
        document.querySelectorAll(".equity").forEach((equity, index) => {
            equity.innerText = `Equity: ${equities[`Jugador ${index+1}`]}%`;
        });
    })
    .catch(error => console.error("Error:", error));
}


