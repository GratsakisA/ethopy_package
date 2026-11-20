# Object experiment task 569 (adding 50/50 obj.)
from ethopy.experiments.match_port import Experiment
from ethopy.behaviors.multi_port import MultiPort
from ethopy.stimuli.tones_panda import TonesPanda
from scipy import interpolate
import time
import random
import numpy as np
from datetime import datetime


interp = lambda x: interpolate.splev(np.linspace(0, len(x), 100),
                            interpolate.splrep(np.linspace(0, len(x), len(x)), x)) if len(x) > 3 else x


# define session parameters
session_params = {
    'setup_conf_idx'        : 0,
    'max_reward'            : 1200,
    'min_reward'            : 700,
    'hydrate_delay'         : 30,
}

exp = Experiment()
exp.setup(logger, MultiPort, session_params)

# ================================================================================================================
exp.interface.give_liquid(1, 100) # keep valve 1 open for 100ms
time.sleep(2) # pause for x(e.g 2) seconds - IMPORTANT OR ELSE VALVES STAY CONSTANTLY OPEN
exp.interface.give_liquid(2, 100) # keep valve 2 open for 100ms
time.sleep(1)
# ================================================================================================================


conditions = []

# define environment conditions
env_key = {
    # Experimental parameters
    'abort_duration'        : 500,
    'punish_duration'       : 10000, 
    'init_ready'            : 50,
    'trial_ready'           : 150,
    'intertrial_duration'   : 500,
    'trial_duration'        : 9000,
    'reward_duration'       : 5000
    }

# env_key = {
#     # Experimental parameters
#     'abort_duration'        : 500,
#     'punish_duration'       : 10000, 
#     'init_ready'            : 0,
#     'trial_ready'           : 0,
#     'intertrial_duration'   : 10,
#     'trial_duration'        : 5,
#     'reward_duration'       : 5000
#     }

print(env_key)

panda_obj = TonesPanda()
panda_obj.fill_colors.set({'background' : (0, 0, 0),
                           'start'      : (0.2, 0.2, 0.2),
                           'reward'     : (0.6, 0.6, 0.6),
                           'punish'     : (0, 0, 0)})



# Difficulty 2 , 

block = exp.Block(difficulty=2, 
                  next_up=2, 
                  next_down=2, 
                  staircase_window=30,
                  trial_selection='random', 
                  stair_up=0.75, 
                  stair_down=0.55, 
                 ) 

# object_ids with corresponding tone_pulse_freq and rew_probe
resp_obj = [218,219,212,213]      
rew_prob = [1,1,2,2]       
tone_pulse_freq = [0,0,100,100]

# ============================== multimodal condition ==============================

multi_cond = []

tone_volume = 20
obj_mag = 0.5 

rot_f = lambda: interp((np.random.rand(20)-.5) *100)
rots = rot_f() # rotation of the object 


for idx, obj_comb in enumerate(resp_obj):
    multi_cond += exp.make_conditions(stim_class=panda_obj, conditions={**env_key, **block.dict(),
          'obj_id'              : resp_obj[idx],
          'obj_dur'             : 9000,
          'obj_pos_x'           : 0, 
          'obj_pos_y'           : 0.02, 
          'obj_mag'             : obj_mag,              # size of the object
          'obj_rot'             : (rots, rots),     # rotation of the object
          'obj_tilt'            : (0,0),            # tilt of the object
          'reward_port'         : rew_prob[idx], 
          'response_port'       : rew_prob[idx], 
          'reward_amount'       : 8,

          'tone_duration'       : 9000,
          'tone_frequency'      : 40500,
          'tone_volume'         : tone_volume,
          'tone_pulse_freq'     : [tone_pulse_freq[idx]]
          })

# ============================== visual condition ==============================

visual_cond = []

tone_volume = 0
obj_mag = 0.5

rot_f = lambda: interp((np.random.rand(20)-.5) *100)
rots = rot_f() # rotation of the object 

for idx, obj_comb in enumerate(resp_obj):
    visual_cond += exp.make_conditions(stim_class=panda_obj, conditions={**env_key, **block.dict(),
          'obj_id'              : resp_obj[idx],
          'obj_dur'             : 9000,
          'obj_pos_x'           : 0, 
          'obj_pos_y'           : 0.02, 
          'obj_mag'             : obj_mag,              # size of the object
          'obj_rot'             : (rots, rots),     # rotation of the object
          'obj_tilt'            : (0,0),            # tilt of the object
          'reward_port'         : rew_prob[idx], 
          'response_port'       : rew_prob[idx], 
          'reward_amount'       : 8,

          'tone_duration'       : 9000,
          'tone_frequency'      : 40500,
          'tone_volume'         : tone_volume,
          'tone_pulse_freq'     : [tone_pulse_freq[idx]]
          })

# ============================== auditory condition ==============================

auditory_cond = []

resp_obj = [218,213]      
rew_prob = [1,2]   
tone_pulse_freq = [0,100]   

tone_volume = 20
obj_mag = 0 

rot_f = lambda: interp((np.random.rand(20)-.5) *100)
rots = rot_f() # rotation of the object 

for idx, obj_comb in enumerate(resp_obj):
    auditory_cond += exp.make_conditions(stim_class=panda_obj, conditions={**env_key, **block.dict(),
          'obj_id'              : resp_obj[idx],
          'obj_dur'             : 9000,
          'obj_pos_x'           : 0, 
          'obj_pos_y'           : 0.02, 
          'obj_mag'             : obj_mag,      
          'obj_rot'             : (rots, rots),     # rotation of the object
          'obj_tilt'            : (0,0),            # tilt of the object
          'reward_port'         : rew_prob[idx], 
          'response_port'       : rew_prob[idx], 
          'reward_amount'       : 8,

          'tone_duration'       : 9000,
          'tone_frequency'      : 40500,
          'tone_volume'         : tone_volume,
          'tone_pulse_freq'     : [tone_pulse_freq[idx]]
          })


# define environment conditions for obj. 50/50
# env50_key = {
#     # Experimental parameters
#     'abort_duration'        : 500,
#     'punish_duration'       : 0, # <---------
#     'init_ready'            : 0,
#     'trial_ready'           : 10,
#     'intertrial_duration'   : 5,
#     'trial_duration'        : 5,
#     'reward_duration'       : 5000
#     }


# ============================== multimodal 50-50 condition ==============================

multi50_cond = []

resp_obj = [215,215]      
rew_prob = [-1,-1]       
tone_pulse_freq = [0,100] 

tone_volume = 20
obj_mag = 0.5  

rot_f = lambda: interp((np.random.rand(20)-.5) *100)
rots = rot_f() # rotation of the object 


for idx, obj_comb in enumerate(resp_obj):
    multi50_cond += exp.make_conditions(stim_class=panda_obj, conditions={**env_key, **block.dict(),
          'obj_id'              : resp_obj[idx],
          'obj_dur'             : 9000,
          'obj_pos_x'           : 0, 
          'obj_pos_y'           : 0.02, 
          'obj_mag'             : obj_mag,              # size of the object
          'obj_rot'             : (rots, rots),     # rotation of the object
          'obj_tilt'            : (0,0),            # tilt of the object
          'reward_port'         : rew_prob[idx], 
          'response_port'       : rew_prob[idx], 
          'reward_amount'       : 0,

          'tone_duration'       : 9000,
          'tone_frequency'      : 40500,
          'tone_volume'         : tone_volume,
          'tone_pulse_freq'     : [tone_pulse_freq[idx]]
          })

# ============================== visual 50-50 condition ==============================

visual50_cond = []

resp_obj = [215]      
rew_prob = [-1]       
tone_pulse_freq = [0] 

tone_volume = 0
obj_mag = 0.5   

rot_f = lambda: interp((np.random.rand(20)-.5) *100)
rots = rot_f() # rotation of the object 


for idx, obj_comb in enumerate(resp_obj):
    visual50_cond += exp.make_conditions(stim_class=panda_obj, conditions={**env_key, **block.dict(),
          'obj_id'              : resp_obj[idx],
          'obj_dur'             : 9000,
          'obj_pos_x'           : 0, 
          'obj_pos_y'           : 0.02, 
          'obj_mag'             : obj_mag,              # size of the object
          'obj_rot'             : (rots, rots),     # rotation of the object
          'obj_tilt'            : (0,0),            # tilt of the object
          'reward_port'         : rew_prob[idx], 
          'response_port'       : rew_prob[idx], 
          'reward_amount'       : 0,

          'tone_duration'       : 9000,
          'tone_frequency'      : 40500,
          'tone_volume'         : tone_volume,
          'tone_pulse_freq'     : [tone_pulse_freq[idx]]
          })


# shuffle conditions
# conditions = multi_cond + multi_cond + visual_cond + visual_cond + auditory_cond + multi50_cond + visual50_cond
conditions = multi_cond + multi_cond + multi_cond + visual_cond + auditory_cond + multi50_cond + visual50_cond


print(f"Total number of trials: {len(conditions)}")
print(f"Multimodal trials: {len(multi_cond)*3}")
print(f"Visual trials: {len(visual_cond)}")
print(f"Auditory trials: {len(auditory_cond)}")
print(f"50-50 Multimodal trials: {len(multi50_cond)}")
print(f"50-50 Visual trials: {len(visual50_cond)}")

# seed_value = int(datetime.now().strftime("%Y%m%d"))
# seed_value = int(datetime.now().timestamp()) % (2**32)
# np.random.seed(seed_value)
# random.shuffle(conditions)

# run experiments
exp.push_conditions(conditions)
exp.start()