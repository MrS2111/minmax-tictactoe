const boardElement = document.getElementById("board");
        const statusElement = document.getElementById("status");
        const restartButton = document.getElementById("restart");
        const backtrackButton = document.getElementById("backtrack");

        const renderBoard = (board) => {
            boardElement.innerHTML = "";
            board.forEach((cell, index) => {
                const cellElement = document.createElement("div");
                cellElement.className = "bg-gray-700 text-white font-bold text-2xl flex items-center justify-center w-16 h-16";
                cellElement.dataset.index = index;
                cellElement.textContent = cell;
                boardElement.appendChild(cellElement);

                cellElement.addEventListener("click", async () => {
                    if (!cellElement.textContent) {
                        const response = await fetch("/move", {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({ index }),
                        });
                        const data = await response.json();
                        renderBoard(data.board);
                        statusElement.textContent = data.winner
                            ? `${data.winner} Wins!`
                            : data.game_over
                            ? "Draw!"
                            : "Your Turn";
                    }
                });
            });
        };

        const restartGame = async () => {
            const response = await fetch("/restart", { method: "POST" });
            const data = await response.json();
            renderBoard(data.board);
            statusElement.textContent = "Your Turn";
        };

        const backtrackMove = async () => {
            const response = await fetch("/backtrack", { method: "POST" });
            const data = await response.json();
            renderBoard(data.board);
            statusElement.textContent = "Your Turn";
        };

        restartButton.addEventListener("click", restartGame);
        backtrackButton.addEventListener("click", backtrackMove);

        restartGame();