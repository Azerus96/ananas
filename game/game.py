from app.game.deck import Deck
from app.game.player import Player
from app.game.ai_player import AIPlayer

class Game:
    def __init__(self, player_names, ai_players=None):
        self.deck = Deck()
        self.players = []
        for name in player_names:
            if ai_players and name in ai_players:
                self.players.append(AIPlayer(name))
            else:
                self.players.append(Player(name))
        self.current_player_index = 0
        self.current_card = None

    def start_round(self):
        self.deck.shuffle()
        for player in self.players:
            player.reset_hand()
        self.deal_initial_cards()
        self.draw_current_card()

    def deal_initial_cards(self):
        for _ in range(5):
            for player in self.players:
                card = self.deck.draw()
                if card:
                    player.hand.add_bottom(card)

    def draw_current_card(self):
        self.current_card = self.deck.draw()

    def play_turn(self, card, position):
        current_player = self.current_player()
        current_player.place_card(card, position)
        self.next_turn()
        self.draw_current_card()

    def next_turn(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def current_player(self):
        return self.players[self.current_player_index]

    def is_round_over(self):
        return all(player.hand.completed for player in self.players)

    def score_round(self):
        for i, player in enumerate(self.players):
            for j, opponent in enumerate(self.players):
                if i != j:
                    points = player.hand.calculate_points(opponent.hand)
                    player.score += points

    def get_game_state(self):
        return {
            'players': [
                {
                    'name': player.name,
                    'hand': str(player.hand),
                    'score': player.score
                } for player in self.players
            ],
            'current_player': self.current_player().name,
            'current_card': str(self.current_card) if self.current_card else None,
            'round_over': self.is_round_over()
        }