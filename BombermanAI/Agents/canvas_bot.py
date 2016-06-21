from .bot import Bot

class CanvasBot(Bot):
    # override constructor := onlt accept a viewer agent
    def __init__(self, agent):
        super().__init__("VIEWER", "VIEWER", agent)

    # override tick() := always send info to agent
    def tick(self, args):
        self.advance_bombs()
        self.agent.next_move(self.map_s, self.players_s, self.bombs)

    # override init := do not register player
    def init(self, args):
        self.agent.init_game()