from .Agents.bot import *
from .Agents.canvas_bot import CanvasBot
from .Agents.human_agent import HumanAgent
from .Agents.greedy_agent import GreedyAgent
from .Agents.random_agent import RandomAgent
from .Viewer.viewer import Viewer
from .Viewer.canvas import MainFrame
from threading import Thread

players = [('YUVAL', '1', GreedyAgent('YUVAL')),
           ('DINA', '2', GreedyAgent('DINA')),
           ('GAL', '3', GreedyAgent('GAL')),
           ('RICK', '4', GreedyAgent('RICK')),
           ('MORTY', '5', GreedyAgent('MORTY'))]

# players = [('YUVAL', '1', HumanAgent()),
#            ('DINA', '2', GreedyAgent('DINA')),
#            ('GAL', '3', GreedyAgent('GAL'))]

def start_player(user, password, agent):
    p = Bot(user, password, agent)

for (user, password, agent) in players:
    t = Thread(target=start_player, args=[user, password, agent])
    t.start()

def viewer_thread(viewer):
    mf = MainFrame(viewer)

# create viewer agent
v = Viewer()
# create main frame thread
t = Thread(target=viewer_thread, args=[v])
t.start()
# put agent in a bot
cnvsbot = CanvasBot(v)