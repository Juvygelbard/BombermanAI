from .Agents.bot import *
from .Agents.canvas_bot import CanvasBot
from .Agents.human_agent import HumanAgent
from .Agents.greedy_agent import GreedyAgent
from .Viewer.viewer import Viewer
from .Viewer.canvas import MainFrame
from .GPUtil.gp_evolution import start_evolution
from threading import Thread

# players = [('YUVAL', '1', GreedyAgent('YUVAL')),
           #('DINA', '2', GreedyAgent('DINA')),
           #('GAL', '3', GreedyAgent('GAL')),
           #('RICK', '4', GreedyAgent('RICK')),
           #('MORTY', '5', GreedyAgent('MORTY'))]

# players = [('YUVAL', '1', HumanAgent()),
#            ('DINA', '2', GreedyAgent('DINA')),
#            ('GAL', '3', GreedyAgent('GAL'))]

players = [('GAL', '3', GreedyAgent('GAL')),
           ('DINA', '2', GreedyAgent('DINA'))]

def start_player(user, password, agent):
    b = Bot(user, password, agent)
    b.connect_and_listen()

for (user, password, agent) in players:
    t = Thread(target=start_player, args=[user, password, agent])
    t.start()

def viewer_thread(viewer):
    mf = MainFrame(viewer)

# start evolution thread
e = Thread(target=start_evolution, args=[20, 20])
e.start()

# # create viewer agent
# v = Viewer()
# # create main frame thread
# t = Thread(target=viewer_thread, args=[v])
# t.start()
#
# # put agent in a bot
# cnvsbot = CanvasBot(v)
# cnvsbot.connect_and_listen()