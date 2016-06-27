from .Agents.greedy_agent import GreedyAgent
from .Agents.human_agent import HumanAgent
from .Agents.gp_agent import GP_Agent
from .Agents.bot import Bot
from .Agents.canvas_bot import CanvasBot
from .Viewer.viewer import Viewer, MainFrame
from threading import Thread
import pickle

PICKLEFILE = 'generation_49.pickle'

f = open(PICKLEFILE, "rb")
generation = pickle.load(f)
f.close()

gp_agent = GP_Agent('RESULT', generation[0])
gp_agent.end_game = lambda p: None

# players = [('GAL', '3', GreedyAgent('GAL'), 'localhost', 8037),
#            ('DINA', '2', GreedyAgent('DINA'), 'localhost', 8037),
#            ('RESULT', 'RESULT', gp_agent, 'localhost', 8037)]

players = [('GAL', '3', HumanAgent(), 'localhost', 8037),
           ('RESULT', 'RESULT', gp_agent, 'localhost', 8037)]

def start_player(user, password, agent, host, port):
    b = Bot(user, password, agent)
    b.connect_and_listen(host, port)

for (user, password, agent, host, port) in players:
    t = Thread(target=start_player, args=[user, password, agent, host, port])
    t.start()

# start viewer
def viewer_thread(viewer):
    mf = MainFrame(viewer)

# create viewer agent
v = Viewer()
# create main frame thread
t = Thread(target=viewer_thread, args=[v])
t.start()

# put agent in a bot
cnvsbot = CanvasBot(v)
cnvsbot.connect_and_listen()