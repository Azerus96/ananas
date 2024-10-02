from app.game.player import Player
from app.utils.hand_ev_estimator import HandEvEstimator, find_optimal_decision
from app.rules.ofc_scoring import Row

class AIPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

    def make_decision(self, game_state, available_card):
        decisions = self.generate_possible_decisions(available_card)
        opponent_hand = next(player['hand'] for player in game_state['players'] if player['name'] != self.name)

        decision_to_ev = find_optimal_decision(self.hand, opponent_hand, decisions)
        best_decision = max(decision_to_ev, key=decision_to_ev.get)

        return best_decision[0]  # Return the first (and only) placement in the best decision

    def generate_possible_decisions(self, available_card):
        decisions = []
        for row in [Row.TOP, Row.MIDDLE, Row.BOTTOM]:
            if not self.hand.is_row_full(row):
                decisions.append([{'card': available_card, 'row': row}])
        return decisions