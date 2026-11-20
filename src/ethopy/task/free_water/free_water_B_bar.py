# task_id: 171

from ethopy.behaviors.multi_port import MultiPort
from ethopy.core.stimulus import Stimulus
from ethopy.experiments.match_port import Experiment
from ethopy.stimuli.bar import Bar
from scipy import interpolate
import time

# define session parameters
session_params = {
    'setup_conf_idx'        : 0, #42
    'max_reward'            : 1200,
    'min_reward'            : 700, 
    'bias_window'           : 5,
    'noresponse_intertrial' : False,
}


exp = Experiment()
exp.setup(logger, MultiPort, session_params)

# ------------------------------------------
exp.interface.give_liquid(1, 200) # keep valve 1 open for 100ms
time.sleep(2) # pause for x(e.g 2) seconds - IMPORTANT OR ELSE VALVES STAY CONSTANTLY OPEN
exp.interface.give_liquid(2, 200) # keep valve 2 open for 100ms
# ------------------------------------------

stim = Stimulus()
stim.fill_colors.set({
    'background': (0, 0, 0),
    'start': (0.2, 0.2, 0.2),
    'ready': (0.3, 0.3, 0.3),
    'reward': (0.6, 0.6, 0.6),
    'punish': (0, 0, 0)
})

block = exp.Block(
    difficulty=-9, 
    next_up=-2, 
    next_down=-2, 
    staircase_window=30, 
    trial_selection='staircase', 
    stair_up=0.75, 
    stair_down=0.55
)

conditions = exp.make_conditions(
    stim_class=stim, 
    conditions={
        **block.dict(), 
        'timeout_duration'   : 0,
        'intertrial_duration': 500,
        'trial_duration'     : 9000,
        'init_ready'         : 50,
        'delay_duration'     : 0,
        'reward_amount'      : 6,
        'reward_port'        : -1, # -1: both port
        'response_port'      : -1, # -1: both port
    }
)


# run experiments
exp.push_conditions(conditions)
exp.start()


