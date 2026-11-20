# Task ID 5202 -- Diff2 & Diff3 -- Rot/Light -- Target Startrek & Dis. Bunnyhead
from ethopy.behaviors.multi_port import MultiPort
from ethopy.experiments.match_port import Experiment
from ethopy.stimuli.panda import Panda
import numpy as np
from scipy import interpolate
import time

interp = lambda x: interpolate.splev(np.linspace(0, len(x), 100),
                                     interpolate.splrep(np.linspace(0, len(x), len(x)), x)) if len(x) > 3 else x

# define session parameters
session_params = {
    'max_reward'            : 1200,
    'min_reward'            : 700,
    'setup_conf_idx'        : 0,
    'hydrate_delay'         : 45,
}


exp = Experiment()
exp.setup(logger, MultiPort, session_params)

exp.interface.give_liquid(1, 300) # keep valve 1 open for 100ms
time.sleep(2) # pause for x(e.g 2) seconds - IMPORTANT OR ELSE VALVES STAY CONSTANTLY OPEN
exp.interface.give_liquid(2, 300) # keep valve 2 open for 100ms

conditions = []

# define environment conditions
env_key = {
    'abort_duration'        : 500,
    'punish_duration'       : 10000,
    'init_ready'            : 100,
    'trial_ready'           : 200,
    'intertrial_duration'   : 500,
    'trial_duration'        : 9000,
    'reward_duration'       : 5000}


print(env_key)

panda_obj = Panda()
panda_obj.fill_colors.set({'background': (0, 0, 0),
                           'start': (0.2, 0.2, 0.2),
                           'reward': (0.6, 0.6, 0.6),
                           'punish': (0, 0, 0)})


# Diff 2 -> distractor + target random rots 
resp_obj = [(2, 1), (1, 2)]
rew_prob = [1, 2]
x_pos = [(-0.3, 0.3), (-0.3, 0.3)]

rot_f = lambda: interp(np.random.rand(20))*100+(np.random.rand(1))*360
repetitions = 100

block = exp.Block(difficulty=2, next_up=3, next_down=2, staircase_window=30, trial_selection='staircase', stair_up=0.75, stair_down=0.55)

for irep in range(repetitions):
    rots = rot_f()
    for idx, obj_comb in enumerate(resp_obj):
        conditions += exp.make_conditions(stim_class=panda_obj, conditions={**env_key, **block.dict(),                                                  
            'obj_id'        : resp_obj[idx],
            'obj_dur'       : 9000,
            'obj_pos_x'     : x_pos[idx],
            'obj_pos_y'     : 0.02,
            'obj_mag'       : 0.5,
            'obj_rot'       : (rots, rots),
            'obj_tilt'      : (0, 0),
            'background_color'  : (0, 0, 0),
            'reward_port'       : rew_prob[idx],
            'response_port'     : rew_prob[idx],
            'reward_amount'     : 6})


# Diff 3 -> distractor + target light
resp_obj = [(2, 1), (1, 2)]
rew_prob = [1, 2]
x_pos = [(-0.3, 0.3), (-0.3, 0.3)]

rot_f = lambda: interp((np.random.rand(20)-.5) *100)
rots = rot_f()

block = exp.Block(difficulty=3, next_up=3, next_down=3, staircase_window=30, trial_selection='staircase', stair_up=0.75, stair_down=0.55)


for idx, obj_comb in enumerate(resp_obj):
    conditions += exp.make_conditions(stim_class=panda_obj, conditions={**env_key, **block.dict(),                                                    
            'obj_id'        : resp_obj[idx],
            'obj_dur'       : 9000,
            'obj_pos_x'     : x_pos[idx],
            'obj_pos_y'     : 0.02,
            'obj_mag'       : 0.5,
            'obj_rot'       : (rots, rots),
            'light_color'   : [(np.array([0.1, 0.1, 0.1, 1]), np.array([0.2, 0.2, 0.2, 1])), (np.array([0.4, 0.4, 0.4, 1]), np.array([0.2, 0.2, 0.2, 1])), (np.array([0.7, 0.7, 0.7, 1]), np.array([0.2, 0.2, 0.2, 1])), (np.array([1, 1, 1, 1]), np.array([0.2, 0.2, 0.2, 1]))],
            'reward_port'       : rew_prob[idx],
            'response_port'     : rew_prob[idx],
            'reward_amount'     : 6})
    



# run experiments
exp.push_conditions(conditions)
exp.start()


