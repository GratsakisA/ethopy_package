# task id 170   --- ruff applied 
import time

from ethopy.behaviors.multi_port import MultiPort
from ethopy.core.stimulus import Stimulus
from ethopy.experiments.free_water import Experiment

# define session parameters
session_params = {
    "setup_conf_idx": 1,
    "max_reward": 700,
    "min_reward": 700,
    "bias_window": 5,
    "noresponse_intertrial": False,
}

exp = Experiment()
exp.setup(logger, MultiPort, session_params)

# activate valves and water supply
exp.interface.give_liquid(1, 100)  # keep valve 1 open for 100ms
time.sleep(2)  # Pause to ensure valve closes
exp.interface.give_liquid(2, 100)  # keep valve 2 open for 100ms

stim = Stimulus()
stim.fill_colors.set(
    {
        "background": (0, 0, 0),
        "start": (0.2, 0.2, 0.2),
        "reward": (0.6, 0.6, 0.6),
        "punish": (0, 0, 0),
    }
)


block = exp.Block(difficulty=-10, trial_selection="biased")

reward_amount = 10

conditions = exp.make_conditions(
    stim_class=stim,
    conditions={
        **block.__dict__,
        "timeout_duration": 0,
        "intertrial_duration": 500,
        "init_duration": 0,
        "delay_duration": 0,
        "reward_amount": reward_amount,
        "reward_port": -1,
        "response_port": -1,
    },
)

# run experiments
exp.push_conditions(conditions)
exp.start()
