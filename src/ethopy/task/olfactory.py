# task id: 1000  — single odor / single delivery port per condition
from ethopy.experiments.match_port import Experiment
from ethopy.behaviors.multi_port import MultiPort
from ethopy.stimuli.olfactory import Olfactory
import time

session_params = {
    'setup_conf_idx'        : 0,
    'max_reward'            : 1200,  # μl
    'min_reward'            : 700,
}

exp = Experiment()
exp.setup(logger, MultiPort, session_params)



exp.interface.give_liquid(1, 200)  # keep valve 1 open for 200ms
time.sleep(2)  # pause - IMPORTANT OR ELSE VALVES STAY CONSTANTLY OPEN
exp.interface.give_liquid(2, 200)  # keep valve 2 open for 200ms
time.sleep(1)

conditions = []

# define environment conditions
env_key = {
    'punish_duration'       : 10000,
    'abort_duration'        : 500,
    'init_ready'            : 100,
    'trial_ready'           : 50,
    'trial_duration'        : 3000,
    'intertrial_duration'   : 1000,
    'response_duration'     : 3000,
    'reward_duration'       : 500,
}

olfactory = Olfactory()
olfactory.fill_colors.set({'background': (0, 0, 0),
                           'start': (0.2, 0.2, 0.2),
                           'ready': (0.3, 0.3, 0.3),
                           'reward': (0.6, 0.6, 0.6),
                           'punish': (0, 0, 0)})

block = exp.Block(
    difficulty=1,
    next_up=1,
    next_down=1,
    staircase_window=30,
    trial_selection='staircase',
    stair_up=0.75,
    stair_down=0.55,
    antibias=True
)

# Difficulty 1 — one odor on one delivery port per condition, always 100% duty
odorants      = [6, 7]   # odor per condition
delivery_port = [1, 2]   # valve per condition (odor 6 -> valve 1, odor 7 -> valve 2)
rew_prob      = [1, 2]   # reward / response port per condition

for idx in range(len(odorants)):
    conditions += exp.make_conditions(
        stim_class=olfactory,
        conditions={
            **env_key,
            **block.dict(),
            'odorant_id':    [[odorants[idx]]],       # e.g. [[6]] -> (6,)
            'odor_duration': 500,
            'delivery_port': [[delivery_port[idx]]],  # e.g. [[1]] -> (1,)
            'dutycycle':     [[100]],                 # single channel at 100%
            'reward_port':   rew_prob[idx],
            'response_port': rew_prob[idx],
            'reward_amount': 6,
        })

print(conditions)

# run experiment
exp.push_conditions(conditions)
exp.start()