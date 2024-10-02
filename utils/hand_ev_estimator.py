from app.game.deck import Deck
from app.rules.ofc_scoring import OfcHand, Row
from itertools import combinations
import random

NUM_EPOCHS = 1000
DRAWS_TO_CARDS = {1: 3, 2: 5, 3: 9, 4: 9}

class HandEvEstimator:
    def __init__(self, our_ofc_hand, their_ofc_hand, dead_cards):
        self.our_ofc_hand = our_ofc_hand
        self.their_ofc_hand = their_ofc_hand
        self.deck = Deck()
        self.deck.remove_cards(dead_cards + our_ofc_hand.all_cards() + their_ofc_hand.all_cards())

        self.our_draws_remaining = (13 - our_ofc_hand.total_cards) // 2
        self.their_draws_remaining = (13 - their_ofc_hand.total_cards) // 2

    def estimate(self, num_epochs=NUM_EPOCHS):
        running_sum = 0
        for _ in range(num_epochs):
            our_cards = self.deck.choose(DRAWS_TO_CARDS[self.our_draws_remaining])
            their_cards = self.deck.choose(DRAWS_TO_CARDS[self.their_draws_remaining])

            our_completed_hand = self.arrange_best_hand(self.our_ofc_hand, our_cards)
            their_completed_hand = self.arrange_best_hand(self.their_ofc_hand, their_cards)

            points = our_completed_hand.calculate_points(their_completed_hand)
            running_sum += points

        return running_sum / num_epochs

    @staticmethod
    def arrange_best_hand(ofc_hand, cards):
        best_hand = None
        best_royalties = -1

        for top_cards in combinations(cards, 3 - ofc_hand.top.total_cards):
            remaining_cards = set(cards) - set(top_cards)
            for middle_cards in combinations(remaining_cards, 5 - ofc_hand.middle.total_cards):
                bottom_cards = remaining_cards - set(middle_cards)

                tmp_hand = OfcHand(
                    ofc_hand.top.row + list(top_cards),
                    ofc_hand.middle.row + list(middle_cards),
                    ofc_hand.bottom.row + list(bottom_cards)
                )

                if not tmp_hand.foul:
                    tmp_royalties = tmp_hand.calculate_total_royalties()
                    if tmp_royalties > best_royalties:
                        best_hand = tmp_hand
                        best_royalties = tmp_royalties

        return best_hand if best_hand else ofc_hand

def find_optimal_decision(our_hand, their_hand, decisions, num_epochs=NUM_EPOCHS):
    decision_to_ev = {}
    for decision in decisions:
        tmp_hand = OfcHand(
            our_hand.top.row.copy(),
            our_hand.middle.row.copy(),
            our_hand.bottom.row.copy()
        )

        for placement in decision:
            if placement['row'] == Row.TOP:
                tmp_hand.add_top(placement['card'])
            elif placement['row'] == Row.MIDDLE:
                tmp_hand.add_middle(placement['card'])
            elif placement['row'] == Row.BOTTOM:
                tmp_hand.add_bottom(placement['card'])

        estimator = HandEvEstimator(tmp_hand, their_hand, [])
        ev = estimator.estimate(num_epochs)
        decision_to_ev[tuple(decision)] = ev

    return decision_to_ev