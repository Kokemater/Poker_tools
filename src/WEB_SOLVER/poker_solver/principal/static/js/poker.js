    const ranks = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"];
        const grid = document.getElementById("pokerGrid");
        const details = document.getElementById("handDetails");

        function createPokerGrid() {
            for (let i = 0; i < ranks.length; i++) {
                for (let j = 0; j < ranks.length; j++) {
                    let hand = document.createElement("div");
                    hand.classList.add("hand");
                    let handName = ranks[i] + ranks[j] + (i < j ? "s" : (i > j ? "o" : ""));
                    hand.textContent = handName;

                    // Asignar colores
                    if (i === j) hand.classList.add("pair");         // Parejas (rojo)
                    else if (i < j) hand.classList.add("suited");   // Suited (verde)
                    else hand.classList.add("offsuited");           // Off-suited (azul)

                    hand.onclick = () => showHandDetails(handName, hand);
                    grid.appendChild(hand);
                }
            }
        }

        function showHandDetails(handName, element) {
            document.querySelectorAll(".hand").forEach(el => el.classList.remove("selected"));
            element.classList.add("selected");

            let suits = ["♠", "♥", "♦", "♣"];
            let combs = [];

            for (let a = 0; a < suits.length; a++) {
                for (let b = 0; b < suits.length; b++) {
                    if (handName.includes("o") && a === b) continue;
                    if (handName.includes("s") && a !== b) continue;
                    if (!handName.includes("o") && !handName.includes("s") && b <= a) continue;
                    combs.push(`${handName[0]}${suits[a]} ${handName[1]}${suits[b]}`);
                }
            }

            details.innerHTML = `<h5 class="text-primary">${handName} - Posibles Combinaciones:</h5>`;
            let table = document.createElement("table");
            table.classList.add("table", "table-bordered", "table-striped", "mt-2");
            let tbody = document.createElement("tbody");
            combs.forEach(comb => { tbody.innerHTML += `<tr><td>${comb}</td></tr>`; });
            table.appendChild(tbody);
            details.appendChild(table);
        }

        createPokerGrid();