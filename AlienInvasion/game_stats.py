class GameStats():
    """Track statistical infomation of the game."""
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False

        # High score should never be reset.
        self.high_score = 0

    def reset_stats(self):
        """Initialize variable statistical information."""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
