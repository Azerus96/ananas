from app.game.card import Rank, Suit

def parse_card(card_str):
    rank_str = card_str[:-1]
    suit_str = card_str[-1]

    rank = next(r for r in Rank if r.name == rank_str)
    suit = next(s for s in Suit if s.value == suit_str)

    return Card(rank, suit)

def cards_to_str(cards):
    return ' '.join(str(card) for card in cards)