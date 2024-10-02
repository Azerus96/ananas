from flask import jsonify, request
from app.game.ai_player import AIPlayer

@bp.route('/distribute_cards', methods=['POST'])
def distribute_cards():
    cards = request.json['cards']
    ai_player = AIPlayer("AI")
    distribution = ai_player.distribute_cards(cards)
    return jsonify(distribution)

@bp.route('/calculate_results', methods=['POST'])
def calculate_results():
    player1 = request.json['player1']
    player2 = request.json['player2']
    player3 = request.json['player3']
    # Здесь должна быть логика проверки рук и подсчета результатов
    # Возвращаем заглушку
    results = {
        'player1': {'score': 10},
        'player2': {'score': 5},
        'player3': {'score': 15}
    }
    return jsonify(results)