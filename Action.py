import numpy as np


class Action:
    """
    Args:
    mean_utility_self (float):  expected utility of an agent's action to itself
    sd_utility_self (float):    standard deviation for generating utility of an agent's action to itself
    mean_utility_other (float): expected utility of an agent's action to other agent
    sd_utility_other (float):   standard deviation for generating utility of an agent's action to other agent
    mean_morality (float):      expected morality value of an agent's action
    sd_morality (float):        standard deviation for generating morality value of an agent's action

    utility_self (float):       utility value of an agent's action to itself
    utility_other (float):      utility value of an agent's action to the other agent
    morality_score (float):     morality value of an agent's action
    """

    def __init__(self, moral_utility_factor, mean_utility_self=0, mean_utility_other=0, mean_morality=0, sd_utility_self=1, sd_utility_other=1, sd_morality=1):
        self.moral_utility_factor = moral_utility_factor
        self.utility_self = np.random.normal(mean_utility_self, sd_utility_self)
        self.utility_other = np.random.normal(mean_utility_other, sd_utility_other)
        self.morality_score = np.random.normal(mean_morality, sd_morality)

        self.utility_self += moral_utility_factor * self.morality_score


