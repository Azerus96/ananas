document.addEventListener('DOMContentLoaded', function() {
    const startGameForm = document.getElementById('start-game-form');
    if (startGameForm) {
        startGameForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const playerName = document.getElementById('player-name').value;
            startGame(playerName);
        });
    }

    const placementButtons = document.querySelectorAll('.placement');
    placementButtons.forEach(button => {
        button.addEventListener('click', function() {
            const position = this.dataset.position;
            makeMove(position);
        });
    });

    // Если мы на странице игры, сразу обновляем состояние
    if (document.getElementById('game-container')) {
        updateGameState();
    }
});

function startGame(playerName) {
    fetch('/start_game', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `player_name=${encodeURIComponent(playerName)}`
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        }
    });
}

function updateGameState() {
    fetch('/game_state')
    .then(response => response.json())
    .then(data => {
        updateUI(data);
    });
}

function makeMove(position) {
    const currentCard = document.getElementById('current-card').dataset.card;
    fetch('/make_move', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `card=${encodeURIComponent(currentCard)}&position=${encodeURIComponent(position)}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateGameState();
            setTimeout(aiMove, 1000);  // Даем небольшую задержку перед ходом AI
        }
    });
}

function aiMove() {
    fetch('/ai_move')
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateGameState();
        }
    });
}

function updateUI(gameState) {
    const playerHand = document.getElementById('player-hand');
    const aiHand = document.getElementById('ai-hand');
    const currentCard = document.getElementById('current-card');
    const placementOptions = document.getElementById('placement-options');

    // Обновляем руки игроков
    playerHand.innerHTML = renderHand(gameState.players[0].hand);
    aiHand.innerHTML = renderHand(gameState.players[1].hand);

    // Обновляем текущую карту
    if (gameState.current_card) {
        currentCard.innerHTML = `Current card: ${gameState.current_card}`;
        currentCard.dataset.card = gameState.current_card;
    } else {
        currentCard.innerHTML = 'No current card';
        currentCard.dataset.card = '';
    }

    // Активируем/деактивируем кнопки размещения
    placementOptions.style.display = gameState.current_player === gameState.players[0].name ? 'flex' : 'none';

    // Обновляем счет
    document.getElementById('player-score').textContent = `Score: ${gameState.players[0].score}`;
    document.getElementById('ai-score').textContent = `Score: ${gameState.players[1].score}`;

    // Проверяем, закончен ли раунд
    if (gameState.round_over) {
        alert('Round over! Scores:\n' +
              `${gameState.players[0].name}: ${gameState.players[0].score}\n` +
              `${gameState.players[1].name}: ${gameState.players[1].score}`);
        // Здесь можно добавить логику для начала нового раунда
    }
}

function renderHand(hand) {
    // Предполагаем, что hand - это строка вида "Ah Ks Qd / 10c 9s 8h / 7d 6c 5s"
    const rows = hand.split(' / ');
    let html = '';
    ['top', 'middle', 'bottom'].forEach((rowName, index) => {
        html += `<div class="${rowName}-row">`;
        rows[index].split(' ').forEach(card => {
            html += `<div class="card">${card}</div>`;
        });
        html += '</div>';
    });
    return html;
}