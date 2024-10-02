from enum import Enum
from app.rules.poker_rules import hand_strength, PokerHand

class Row(Enum):
    TOP = 0
    MIDDLE = 1
    BOTTOM = 2

class OfcHand:
    def __init__(self, top=None, middle=None, bottom=None):
        self.top = top or []
        self.middle = middle or []
        self.bottom = bottom or []

    def add_top(self, card):
        if len(self.top) < 3:
            self.top.append(card)
        else:
            raise ValueError("Top row is full")

    def add_middle(self, card):
        if len(self.middle) < 5:
            self.middle.append(card)
        else:
            raise ValueError("Middle row is full")

    def add_bottom(self, card):
        if len(self.bottom) < 5:
            self.bottom.append(card)
        else:
            raise ValueError("Bottom row is full")

    @property
    def total_cards(self):
        return len(self.top) + len(self.middle) + len(self.bottom)

    @property
    def completed(self):
        return len(self.top) == 3 and len(self.middle) == 5 and len(self.bottom) == 5

    @property
    def foul(self):
        if not self.completed:
            return False
        return not (hand_strength(self.top) <= hand_strength(self.middle) <= hand_strength(self.bottom))

    def calculate_royalties(self):
        royalties = 0
        if not self.foul:
            royalties += self._row_royalties(self.top, Row.TOP)
            royalties += self._row_royalties(self.middle, Row.MIDDLE)
            royalties += self._row_royalties(self.bottom, Row.BOTTOM)
        return royalties

    def _row_royalties(self, row, row_type):
        strength = hand_strength(row)
        if row_type == Row.TOP:
            if strength == PokerHand.TRIPS:
                return 10 + max(card.rank.value for card in row)
            elif strength == PokerHand.PAIR:
                pair_rank = max(card.rank.value for card in row if row.count(card) == 2)
                if pair_rank >= 6:  # 6s or higher
                    return pair_rank - 5
            return 0
        elif row_type == Row.MIDDLE:
            royalties = {
                PokerHand.STRAIGHT: 4,
                PokerHand.FLUSH: 8,
                PokerHand.FULL_HOUSE: 12,
                PokerHand.QUADS: 20,
                PokerHand.STRAIGHT_FLUSH: 30,
                PokerHand.ROYAL_FLUSH: 50
            }
            return royalties.get(strength, 0)
        elif row_type == Row.BOTTOM:
            royalties = {
                PokerHand.STRAIGHT: 2,
                PokerHand.FLUSH: 4,
                PokerHand.FULL_HOUSE: 6,
                PokerHand.QUADS: 10,
                PokerHand.STRAIGHT_FLUSH: 15,
                PokerHand.ROYAL_FLUSH: 25
            }
            return royalties.get(strength, 0)

    def calculate_points(self, other):
        if self.foul and other.foul:
            return 0
        elif self.foul:
            return -6 - other.calculate_royalties()
        elif other.foul:
            return 6 + self.calculate_royalties()

        points = 0
        royalties_diff = self.calculate_royalties() - other.calculate_royalties()
        points += royalties_diff

        for our_row, their_row in zip([self.top, self.middle, self.bottom],
                                      [other.top, other.middle, other.bottom]):
            if hand_strength(our_row) > hand_strength(their_row):
                points += 1
            elif hand_strength(our_row) < hand_strength(their_row):
                points -= 1

        if all(hand_strength(our_row) > hand_strength(their_row)
               for our_row, their_row in zip([self.top, self.middle, self.bottom],
                                             [other.top, other.middle, other.bottom])):
            points += 3  # scoop bonus

        return points

    def __str__(self):
        return f"{' '.join(str(card) for card in self.top)} / " \
               f"{' '.join(str(card) for card in self.middle)} / " \
               f"{' '.join(str(card) for card in self.bottom)}"

    def all_cards(self):
        return self.top + self.middle + self.bottom