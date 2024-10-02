from enum import Enum
from collections import defaultdict

class PokerHand(Enum):
    HIGH_CARD = 0
    PAIR = 1
    TWO_PAIR = 2
    TRIPS = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    QUADS = 7
    STRAIGHT_FLUSH = 8
    ROYAL_FLUSH = 9

def hand_strength(hand):
    freq = defaultdict(int)
    for card in hand:
        freq[card.rank.value] += 1
    sorted_values = sorted(freq.values())

    is_flush = len(set(card.suit for card in hand)) == 1
    is_straight = check_straight(hand)

    if is_straight and is_flush:
        if max(card.rank.value for card in hand) == 14:  # Ace
            return PokerHand.ROYAL_FLUSH
        return PokerHand.STRAIGHT_FLUSH

    if sorted_values == [1, 4]:
        return PokerHand.QUADS
    if sorted_values == [2, 3]:
        return PokerHand.FULL_HOUSE
    if is_flush:
        return PokerHand.FLUSH
    if is_straight:
        return PokerHand.STRAIGHT
    if sorted_values == [1, 1, 3]:
        return PokerHand.TRIPS
    if sorted_values == [1, 2, 2]:
        return PokerHand.TWO_PAIR
    if sorted_values == [1, 1, 1, 2]:
        return PokerHand.PAIR
    return PokerHand.HIGH_CARD

def check_straight(hand):
    values = sorted(card.rank.value for card in hand)
    if values == [2, 3, 4, 5, 14]:  # Ace-low straight
        return True
    return max(values) - min(values) == 4 and len(set(values)) == 5