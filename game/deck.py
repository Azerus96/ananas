from app.game.card import Card, Rank, Suit
import random

class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for rank in Rank for suit in Suit]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop() if self.cards else None

    def remove_cards(self, cards):
        for card in cards:
            if card in self.cards:
                self.cards.remove(card)

    def choose(self, k):
        return random.sample(self.cards, k)