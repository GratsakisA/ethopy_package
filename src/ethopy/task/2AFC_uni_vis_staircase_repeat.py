# experiment task 209
# visual stimuli: morphs 212, 213, 218 and 219
# repeat trials: This task is with repeated trials in case of incorrect response
# It consists of three difficulty levels
# difficulty -2: obj. 212 and 219
# difficulty -1: obj. 213 and 218
# difficulty 1: obj. 212, 213, 218 and 219 and stay in this difficulty level

from ethopy.experiments.match_port import Experiment
from ethopy.behaviors.multi_port import MultiPort
from ethopy.stimuli.panda import Panda
from scipy import interpolate
import time
import random
import numpy as np
from datetime import datetime



#----------------------------------------(repeat trials)
def _get_new_cond_f(self):
    if self.curr_cond['trial_selection'] == 'staircase':
        perf, choice_h = self._get_performance()
        if np.size(self.beh.choice_history) and self.beh.choice_history[-1:][0] > 0:
            self.cur_block_sz += 1  # current block trial counter
        if self.cur_block_sz >= self.curr_cond['staircase_window']:
            if perf >= self.curr_cond['stair_up']:
                self.cur_block = self.curr_cond['next_up']
                self.cur_block_sz = 0
                self.logger.update_setup_info({'difficulty': self.cur_block})
            elif perf < self.curr_cond['stair_down']:
                self.cur_block = self.curr_cond['next_down']
                self.cur_block_sz = 0
                self.logger.update_setup_info({'difficulty': self.cur_block})
        if self.curr_cond['antibias']:
            anti_bias = self._anti_bias(choice_h, self.un_choices[self.un_blocks == self.cur_block])
            condition_idx = np.logical_and(self.choices == anti_bias, self.blocks == self.cur_block)
        else: condition_idx = self.blocks == self.cur_block
        # Do not repeat condition if it was the last trial of the block
        if self.curr_cond['repeat_trial'] and self.cur_block_sz:
            if np.size(self.beh.choice_history) and self.beh.choice_history[-1:][0] > 0:
                if ~np.isnan(self.beh.punish_history[-1]): self.repeat_trial=1
                else: self.repeat_trial=0
            if self.repeat_trial:
                self.block_h.append(self.cur_block)
                return
        self.curr_cond = np.random.choice([i for (i, v) in zip(self.conditions, condition_idx) if v])
        self.block_h.append(self.cur_block)
@dataclass
class Block_f:
    difficulty: int = field(compare=True, default=0, hash=True)
    stair_up: float = field(compare=False, default=.7)
    stair_down: float = field(compare=False, default=0.55)
    next_up: int = field(compare=False, default=0)
    next_down: int = field(compare=False, default=0)
    staircase_window: int = field(compare=False, default=20)
    bias_window: int = field(compare=False, default=5)
    trial_selection: str = field(compare=False, default='fixed')
    metric: str = field(compare=False, default='accuracy')
    antibias: bool = field(compare=False, default=True)
    noresponse_intertrial: bool = field(compare=False, default=True)
    incremental_punishment: bool = field(compare=False, default=False)
    repeat_trial: bool = field(compare=False, default=False)
    def dict(self):
        return self.__dict__


interp = lambda x: interpolate.splev(np.linspace(0, len(x), 100),
                            interpolate.splrep(np.linspace(0, len(x), len(x)), x)) if len(x) > 3 else x


# define session parameters
session_params = {
    'setup_conf_idx'        : 0, # idx 7 is for camera
    'max_reward'            : 1200,
    'min_reward'            : 700,
    'hydrate_delay'         : 30,
}

exp = Experiment()
exp.setup(logger, MultiPort, session_params)

ExperimentClass._get_new_cond=_get_new_cond_f
exp.Block=Block_f     
exp.repeat_trial=0

exp.interface.give_liquid(1, 200) # keep valve 1 open for 100ms
time.sleep(2) # pause for x(e.g 2) seconds - IMPORTANT OR ELSE VALVES STAY CONSTANTLY OPEN
exp.interface.give_liquid(2, 200) # keep valve 2 open for 100ms

conditions = []

# define environment conditions
env_key = {
    'init_ready'            : 50,
    'trial_ready'           : 100,
    'abort_duration'        : 500,
    'punish_duration'       : 10000,
    'reward_duration'       : 5000,
    'intertrial_duration'   : 500,
    'trial_duration'        : 9000,
    }

print(env_key)

panda_obj = Panda()
panda_obj.fill_colors.set(
    {
        'background' : (0, 0, 0),
        'start'      : (0.2, 0.2, 0.2),
        'ready'      : (0.3, 0.3, 0.3),
        'reward'     : (0.6, 0.6, 0.6),
        'punish'     : (0, 0, 0)
    }
)

reward_amount = 6

# Difficulty -2
resp_obj = [219,212]      
rew_prob = [1,2]          

rot_f = lambda: interp((np.random.rand(20)-.5) *100)
rots = rot_f() # rotation of the object 

block = exp.Block(
    difficulty=-2, 
    next_up=-1, 
    next_down=-2, 
    staircase_window=30,
    trial_selection='staircase', 
    stair_up=0.75, 
    stair_down=0.55,
    incremental_punishment=False,
    antibias=False,
    repeat_trial=True
) 

for idx, obj_comb in enumerate(resp_obj):
  conditions += exp.make_conditions(
      stim_class=panda_obj, 
      conditions={
          **env_key, 
          **block.dict(),                                               
          'obj_id'              : resp_obj[idx],
          'obj_dur'             : 9000,
          'obj_pos_x'           : 0,
          'obj_pos_y'           : 0.02,
          'obj_mag'             : 0.5,              # size of the object
          'obj_rot'             : (rots, rots),     # rotation of the object
          'obj_tilt'            : (0,0),            # tilt of the object
          'reward_port'         : rew_prob[idx], 
          'response_port'       : rew_prob[idx], 
          'reward_amount'       : reward_amount
      }
  )


# Difficulty -1
resp_obj = [218,213]      
rew_prob = [1,2]       

rot_f = lambda: interp((np.random.rand(20)-.5) *100)
rots = rot_f() # rotation of the object 

block = exp.Block(
    difficulty=-1, 
    next_up=1, 
    next_down=-2, 
    staircase_window=30,
    trial_selection='staircase', 
    stair_up=0.75, 
    stair_down=0.55,
    incremental_punishment=False,
    antibias=False,
    repeat_trial=True
)

for idx, obj_comb in enumerate(resp_obj):
  conditions += exp.make_conditions(
      stim_class=panda_obj, 
      conditions={
          **env_key, 
          **block.dict(),                                               
          'obj_id'              : resp_obj[idx],
          'obj_dur'             : 9000,
          'obj_pos_x'           : 0,
          'obj_pos_y'           : 0.02,
          'obj_mag'             : 0.5,              # size of the object
          'obj_rot'             : (rots, rots),     # rotation of the object
          'obj_tilt'            : (0,0),            # tilt of the object
          'reward_port'         : rew_prob[idx], 
          'response_port'       : rew_prob[idx], 
          'reward_amount'       : reward_amount
      }
  )



# Difficulty 1
resp_obj = [219,218,212,213]      
rew_prob = [1,1,2,2]         

rot_f = lambda: interp((np.random.rand(20)-.5) *100)
rots = rot_f() # rotation of the object 

block = exp.Block(
    difficulty=1, 
    next_up=1, 
    next_down=1, 
    staircase_window=30,
    trial_selection='staircase', 
    stair_up=0.75, 
    stair_down=0.55,
    incremental_punishment=False,
    antibias=False,
    repeat_trial=True
)

for idx, obj_comb in enumerate(resp_obj):
  conditions += exp.make_conditions(
      stim_class=panda_obj, 
      conditions={
          **env_key, 
          **block.dict(),                                               
          'obj_id'              : resp_obj[idx],
          'obj_dur'             : 9000,
          'obj_pos_x'           : 0,
          'obj_pos_y'           : 0.02,
          'obj_mag'             : 0.5,              # size of the object
          'obj_rot'             : (rots, rots),     # rotation of the object
          'obj_tilt'            : (0,0),            # tilt of the object
          'reward_port'         : rew_prob[idx], 
          'response_port'       : rew_prob[idx], 
          'reward_amount'       : reward_amount
      }
  )


seed_value = int(datetime.now().strftime("%Y%m%d"))
# seed_value = int(datetime.now().timestamp()) % (2**32)
np.random.seed(seed_value)

# run experiments
exp.push_conditions(conditions)
exp.start()