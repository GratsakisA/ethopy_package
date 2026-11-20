# Task 8589: 8 different rotation angles, yaws, mags, tilts and lights in blocks

# Object experiment 2AFC for neuropixels
from ethopy.experiments.match_port import Experiment
from ethopy.behaviors.multi_port import MultiPort
from ethopy.stimuli.panda import Panda
from scipy import interpolate
import time
import numpy as np

interp = lambda x: interpolate.splev(np.linspace(0, len(x), 100),
                                     interpolate.splrep(np.linspace(0, len(x), len(x)), x)) if len(x) > 3 else x


# define session parameters
session_params = {
    'setup_conf_idx'        : 0,
    'max_reward'            : 1200,
    'min_reward'            : 700,
    'hydrate_delay'         : 40, ## 40 minutes after the offtime??
    'noresponse_intertrial' : True, # default: False    
}

exp = Experiment()
exp.setup(logger, MultiPort, session_params)

## this is to initiate the valves
exp.interface.give_liquid(1, 100) # keep valve 1 open for 100ms
time.sleep(2) # pause for x(e.g 2) seconds - IMPORTANT OR ELSE VALVES STAY CONSTANTLY OPEN
exp.interface.give_liquid(2, 100) # keep valve 2 open for 100ms

conditions = []

# define environment conditions
env_key = {
    # Experimental parameters
    'abort_duration'        : 500,
    'punish_duration'       : 10000,
    'init_ready'            : 50, # 100
    'trial_ready'           : 200, # 150 
    'intertrial_duration'   : 1000,
    'trial_duration'        : 9000,
    'reward_duration'       : 5000,
    }

print(env_key)

panda_obj = Panda()
panda_obj.fill_colors.set({'background' : (0, 0, 0),
                           'start'      : (0.2, 0.2, 0.2),
                           'ready'      : (0, 0, 0),
                           'reward'     : (0.6, 0.6, 0.6),
                           'punish'     : (0, 0, 0)})




resp_obj = [1,2]       # target object (1 or 2)
rew_prob = [1,2]       # which port to reward (1 or 2)
reward_amount = 6

np.random.seed(0) ## to ensure the first rot is always the same
rot_f = lambda: interp((np.random.rand(20)-.5) *100)
the_rot = rot_f() # initial rotation of the object 
rot_angles = [0, 45, 90, 135, 180, 225, 270, 315]
# the_mags = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
# lights = [[(np.array([0, -20, 0]), np.array([180, -20, 0]))],
#           [(np.array([0, 20, 0]), np.array([180, 20, 0]))],
#           [(np.array([0, -50, 0]), np.array([180, -50, 0]))],
#           [(np.array([0, 50, 0]), np.array([180, 50, 0]))],
#           [(np.array([0, -90, 0]), np.array([180, -90, 0]))],
#           [(np.array([0, 90, 0]), np.array([180, 90, 0]))],
#          ]


# Difficulty 1 - rot + yaw
block = exp.Block(difficulty=1, 
                  next_up=2, 
                  next_down=1, 
                  staircase_window=10, # default: 20
                  trial_selection='staircase', 
                  stair_up=0.75, 
                  stair_down=0.5, 
                  antibias=True, # default: True
                  bias_window=5, # default: 5
                  # incremental_punishment=False,
                 ) 


for irot in rot_angles:
    rots = the_rot + irot
    for idx, obj_comb in enumerate(resp_obj):
      conditions += exp.make_conditions(stim_class=panda_obj, conditions={**env_key, **block.dict(),            
              'obj_id'              : resp_obj[idx],
              'obj_dur'             : 9000,
              'obj_pos_x'           : 0,
              'obj_pos_y'           : 0.02,
              'obj_mag'             : 0.5,              # size of the object
              'obj_rot'             : (rots, rots),     # rotation of the object
              'obj_yaw'             : (rots, rots),     # rotation of the object
              'obj_tilt'            : (0,0),            # tilt of the object
              'reward_port'         : rew_prob[idx], 
              'response_port'       : rew_prob[idx], 
              'reward_amount'       : reward_amount,
              })


# Difficulty 2 - rot + tilt
block = exp.Block(difficulty=2, 
                  next_up=3, 
                  next_down=1, 
                  staircase_window=10, # default: 20
                  trial_selection='staircase', 
                  stair_up=0.75, # 
                  stair_down=0.5, 
                  antibias=True, # default: True
                  bias_window=5, # default: 5
                  # incremental_punishment=False,
                 ) 

for irot in rot_angles:
    rots = the_rot + irot
    for idx, obj_comb in enumerate(resp_obj):
      conditions += exp.make_conditions(stim_class=panda_obj, conditions={**env_key, **block.dict(),            
              'obj_id'              : resp_obj[idx],
              'obj_dur'             : 9000,
              'obj_pos_x'           : 0,
              'obj_pos_y'           : 0.02,
              'obj_mag'             : 0.5,              # size of the object
              'obj_rot'             : (rots, rots),     # rotation of the object
              'obj_yaw'             : (0, 0),     # rotation of the object
              'obj_tilt'            : (rots, rots),            # tilt of the object
              'reward_port'         : rew_prob[idx], 
              'response_port'       : rew_prob[idx], 
              'reward_amount'       : reward_amount,
              })


# Difficulty 3 - tilt + yaw
block = exp.Block(difficulty=3, 
                  next_up=1, 
                  next_down=2, 
                  staircase_window=10, # default: 20
                  trial_selection='staircase', 
                  stair_up=0.75, # 
                  stair_down=0.5, 
                  antibias=True, # default: True
                  bias_window=5, # default: 5
                  # incremental_punishment=False,
                 ) 

for irot in rot_angles:
    rots = the_rot + irot
    for idx, obj_comb in enumerate(resp_obj):
      conditions += exp.make_conditions(stim_class=panda_obj, conditions={**env_key, **block.dict(),            
              'obj_id'              : resp_obj[idx],
              'obj_dur'             : 9000,
              'obj_pos_x'           : 0,
              'obj_pos_y'           : 0.02,
              'obj_mag'             : 0.5,              # size of the object
              'obj_rot'             : (0, 0),     # rotation of the object
              'obj_yaw'             : (rots, rots),     # rotation of the object
              'obj_tilt'            : (rots, rots),            # tilt of the object
              'reward_port'         : rew_prob[idx], 
              'response_port'       : rew_prob[idx], 
              'reward_amount'       : reward_amount,
              })
        
        
# run experiments
exp.push_conditions(conditions)
exp.start()