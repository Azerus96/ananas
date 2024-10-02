from app.rules.ofc_scoring import OfcHand

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = OfcHand()
        self.score = 0

    def reset_hand(self):
        self.hand = OfcHand()

    def place_card(self, card, position):
        if position == 'top':
            self.hand.add_top(card)
        elif position == 'middle':
            self.hand.add_middle(card)
        elif position == 'bottom':
            self.hand.add_bottom(card)
        else:
            raise ValueError("Invalid position")