from Action import Action
import numpy as np
from random import randint


class Agent:
    '''
    Args:
    moral_type =            "kant","util","ego","altr","rnd","psyc"
    n_agents_per_type =     number of agents per type
    threshold_make_break =  threshold of total utility - staying or breaking up
    moral_utility_factor =  how much morallity adds to utility
    ... args of actions of agent ...
    '''

    def __init__(self, id, moral_type, moral_utility_factor, threshold_make_break, mean_utility_self=0, mean_utility_other=0, mean_morality=0, sd_utility_self=1, sd_utility_other=1, sd_morality=1, n_action_freedom = 10):
        self.id = id
        self.moral_type = moral_type
        self.moral_utility_factor = moral_utility_factor
        self.threshold_make_break = threshold_make_break
        self.mean_utility_self = mean_utility_self
        self.mean_utility_other = mean_utility_other
        self.mean_morality = mean_morality
        self.sd_utility_self = sd_utility_self
        self.sd_utility_other = sd_utility_other
        self.sd_morality = sd_morality
        self.n_action_freedom = n_action_freedom
        self.past_actions = []
        self.agent_total_utility = 0 # given both by self and by other
        self.average_morality = 0

    def choose_action(self):
        # set possible action alternative for agent's next step
        action_alternatives = []
        for i in range(self.n_action_freedom):
            action_alternatives.append(Action(self.moral_utility_factor, self.mean_utility_self, self.mean_utility_other, self.mean_morality, self.sd_utility_self, self.sd_utility_other, self.sd_morality))

        # choose best action according to agent's morality
        if self.moral_type == "kant":
            # A Kantian chooses the action that maximizes universal morality, regardless of utility
            self.current_action = max(action_alternatives, key=lambda x: x.morality_score)

        elif self.moral_type == "util":
            # A Utilitarian chooses the action that maximizes the couple's total utility
            self.current_action = max(action_alternatives, key=lambda x: (x.utility_self + x.utility_other))

        elif self.moral_type == "ego":
            # An Egoist chooses the action that maximizes its utility
            self.current_action = max(action_alternatives, key=lambda x: x.utility_self)

        elif self.moral_type == "altr":
            # An Altruist chooses the action that maximizes its utility
            self.current_action = max(action_alternatives, key=lambda x: x.utility_other)

        elif self.moral_type == "psyc":
            # A Psychopath chooses the action that
            # maximizes its utility, minimizes the other's utility and minimizes morality
            self.current_action = max(action_alternatives, key=lambda x: x.utility_self - x.utility_other - x.morality_score)

        elif self.moral_type == "rnd":
            # An agent with no moral that makes decisions by a coin flip
            self.current_action = action_alternatives[randint(0,self.n_action_freedom-1)]

        self.past_actions.append(self.current_action)

        self.average_utility_on_self = sum(act.utility_self for act in self.past_actions) / len(self.past_actions)
        self.average_utility_on_other = sum(act.utility_other for act in self.past_actions) / len(self.past_actions)
        self.average_morality = sum(act.morality_score for act in self.past_actions) / len(self.past_actions)


    def set_agent_total_utility(self,agent_total_utility):
        self.agent_total_utility = agent_total_utility
