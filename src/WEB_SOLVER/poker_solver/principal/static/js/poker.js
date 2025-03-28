const ranks = ["a", "k", "q", "j", "t", "9", "8", "7", "6", "5", "4", "3", "2"];
const grid = document.getElementById("pokerGrid");
const details = document.getElementById("handDetails");

console.log(datos);


let recommendedPlays = {};  // Diccionario para almacenar las jugadas recomendadas

function createPokerGrid() {
    for (let i = 0; i < ranks.length; i++) {
        for (let j = 0; j < ranks.length; j++) {
            let hand = document.createElement("div");
            let handName = ranks[i] + ranks[j] + (i < j ? "s" : (i > j ? "o" : ""));
            hand.classList.add("hand");
            hand.textContent = handName;
            hand.onclick = () => showHandDetails(handName, hand);
            grid.appendChild(hand);
        }
    }
}

function showHandDetails(handName, element) {
    document.querySelectorAll(".hand").forEach(el => el.classList.remove("selected"));
    element.classList.add("selected");

    let suits = ["s", "h", "d", "c"];
    let combs = [];

    // Limpiar posibles combinaciones previas y la jugada recomendada
    details.innerHTML = `<h5 class="text-primary">${handName} | Jugada recomendada</h5>`;
    
    // Crear la tabla si no existe
    let table = document.createElement("table");
    table.classList.add("table", "table-bordered", "table-striped", "mt-2");
    let tbody = document.createElement("tbody");
    table.appendChild(tbody);
    details.appendChild(table);
    
    // Generar las combinaciones de cartas y asignar IDs únicos
    for (let a = 0; a < suits.length; a++) {
        for (let b = 0; b < suits.length; b++) {
            if (handName.includes("o") && a === b) continue;
            if (handName.includes("s") && a !== b) continue;
            if (!handName.includes("o") && !handName.includes("s") && b <= a) continue;
            
            let comb = `${handName[0]}${suits[a]} ${handName[1]}${suits[b]}`;
            combs.push(comb);
            
            // Crear un ID único para cada combinación
            let combId = `${comb.replace(" ", "_")}`;
            
            // Crear fila para la tabla
            let row = document.createElement("tr");
            row.id = combId;
            
            // Agregar la combinación de cartas a la celda
            let combCell = document.createElement("td");
            combCell.textContent = comb;
            row.appendChild(combCell);

            // Crear un sub-div para la jugada recomendada
            let recommendationCell = document.createElement("td");
            let recommendationDiv = document.createElement("div");
            recommendationDiv.classList.add("recommendation");
            recommendationDiv.textContent = datos[combId];  // Inicialmente vacío
            recommendationCell.appendChild(recommendationDiv);
            row.appendChild(recommendationCell);
            tbody.appendChild(row);
        }
    }
}

function updateGridInfo(data) {
    Object.entries(data).forEach(([handNotation, info]) => {
        let cards = handNotation.split(" "); // Separar las dos cartas
        let rank1 = cards[0][0]; // Tomar solo el número/letra de la primera carta
        let rank2 = cards[1][0]; // Tomar solo el número/letra de la segunda carta

        let handID = rank1 + rank2;
        if (ranks.indexOf(rank1) < ranks.indexOf(rank2)) {
            handID += "s"; // Suited
        } else if (ranks.indexOf(rank1) > ranks.indexOf(rank2)) {
            handID += "o"; // Off-suited
        }

        let cell = document.getElementById(handID);
        if (cell) {
            let infoDiv = cell.querySelector(".hand-info");
            if (infoDiv) {
                infoDiv.textContent = info;  // Actualizar subcelda con la información
            }
        }
    });
}

createPokerGrid();
