from Agent import Agent
from random import randint


class Couple:
    '''
    Args:
    two agents


    '''

    def __init__(self, agent_a, agent_b):
        self.agent_a = agent_a
        self.agent_b = agent_b
        self.is_active = True
        self.couple_n_steps = 0
        self.couple_average_utility = 0
        self.couple_average_morality = 0

    def run_step(self):
        self.agent_a.choose_action()
        self.agent_b.choose_action()

    def make_or_break(self):
        # Both agents decide whether to continue the relationship or break up
        # A break up occurs if at least one agent decides to break up
        self.agent_make_or_break(self.agent_a, self.agent_b)
        self.agent_make_or_break(self.agent_b, self.agent_a)
        self.couple_average_utility = (self.agent_a.agent_total_utility + self.agent_b.agent_total_utility) / 2
        self.couple_average_morality = (self.agent_a.average_morality + self.agent_b.average_morality) / 2
        self.couple_n_steps += 1

    def agent_make_or_break(self, agent_a, agent_b):
        # agent_a decides whether to continue the relationship or break up

        self.agent_a.set_agent_total_utility((self.agent_a.average_utility_on_self + self.agent_b.average_utility_on_other) / 2)
        self.agent_b.set_agent_total_utility((self.agent_b.average_utility_on_self + self.agent_a.average_utility_on_other) / 2)


        if self.agent_a.moral_type == "kant":
            # A Kantian
            if self.agent_a.agent_total_utility < self.agent_a.threshold_make_break or self.agent_b.agent_total_utility < self.agent_a.threshold_make_break:
                self.is_active = False

        elif self.agent_a.moral_type == "util":
            # A Utilitarian
            couple_mean_utility = (self.agent_a.agent_total_utility + self.agent_b.agent_total_utility) / 2
            if couple_mean_utility < self.agent_a.threshold_make_break:
                self.is_active = False

        elif self.agent_a.moral_type == "ego":
            # An Egoist
            if self.agent_a.agent_total_utility < self.agent_a.threshold_make_break:
                self.is_active = False

        elif self.agent_a.moral_type == "altr":
            # An Altruist
            if self.agent_b.agent_total_utility < self.agent_a.threshold_make_break:
                self.is_active = False

        elif self.agent_a.moral_type == "psyc":
            # A Psychopath
            if self.agent_a.agent_total_utility < self.agent_a.threshold_make_break and self.agent_b.agent_total_utility > self.agent_a.threshold_make_break:
                self.is_active = False


        elif self.agent_a.moral_type == "rnd":
            # An agent with no moral that makes decisions by a coin flip
            if randint(0,1) < 0.5:
                self.is_active = False

