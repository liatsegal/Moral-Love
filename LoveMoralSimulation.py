from Action import Action
from Agent import Agent
from Couple import Couple
from random import shuffle
import numpy as np
import matplotlib.pyplot as plt
from time import gmtime


###### PARAMETERS ######
"""
simulation_mode =
           "real": couples form out of current singles,
           "theoretical": each round one couple is selected out of entire population
number_of_rounds_at_theoretical_simulation =  when simulation_mode="theoretical" - the number of couples to test
number_of_steps =       ("real") steps of simulation OR ("theoretical") maximum steps for round

moral_type =            "kant","util","ego","altr","rnd","psyc"
n_agents_per_type =     number of agents per type
threshold_make_break =  threshold of total utility - staying or breaking up
moral_utility_factor =  how much morallity adds to utility
"""

simulation_mode = "theoretical"
number_of_rounds_at_theoretical_simulation = 1000
number_of_steps = 1000

moral_type =                ("kant",    "util",         "ego",      "altr",      "rnd",         "psyc")
n_agents_per_type =         (100,       100,            100,        100,        100,            100)
threshold_make_break =      (0.5,          1.5,          0.8,        0.8,        0.5,            0.5)
moral_utility_factor =      (1.5,         0.5,            0.3,        0.7,        0.5,            -0.5)

moral_title =               ("Kantian", "Utilitarian",  "Egoist",   "Altruist", "CoinFlipper",  "Psychopath")


###### MAIN ######


n_of_types = len(n_agents_per_type)

# Initiate agents
all_agents = []
agent_id_counter = 0

# Construct agents:
for t in range(n_of_types):
    for i in range(n_agents_per_type[t]):
        all_agents.append(Agent(agent_id_counter, moral_type[t], moral_utility_factor[t], threshold_make_break[t]))
        agent_id_counter += 1

# remove last agent if the total number of agents is odd
if len(all_agents) % 2 == 1:
    all_agents = all_agents[:len(all_agents)-1]

# Initiate couples
number_of_agents = agent_id_counter
singles_ids = list(range(number_of_agents))
active_couples = []
history_couples = []

### run simulation ###
if simulation_mode == "real":
    for s in range(number_of_steps):
        print("--------- Step %s\t" % s)
        # make new couples
        shuffle(singles_ids)
        while len(singles_ids)>0:
            # new couple's ids
            id_a = singles_ids.pop()
            id_b = singles_ids.pop()

            # make new couple
            active_couples.append(Couple(all_agents[id_a], all_agents[id_b]))

        # run agents' actions
        # (at each step all agents are coupled)
        for ac in active_couples:
            ac.run_step()
            ac.make_or_break()

            # if couple broke up
            if not ac.is_active:
                singles_ids.append(ac.agent_a.id)
                singles_ids.append(ac.agent_b.id)

                history_couples.append(ac)
                active_couples.remove(ac)

            #print("id_a=%s [%s]\tid_b=%s [%s]\tis_active=%s\tn_steps=%s" % (ac.agent_a.id, ac.agent_a.moral_type, ac.agent_b.id, ac.agent_b.moral_type, ac.is_active, ac.couple_n_steps))

    # at the end of the simulation add active couples to history log
    for ac in active_couples:
        history_couples.append(ac)

    #for hc in history_couples:
        #print("%s\t\t%s\t\t%s\t\t%s\t" % (hc.agent_a.moral_type, hc.agent_b.moral_type, hc.couple_n_steps , hc.agent_a.agent_total_utility + hc.agent_b.agent_total_utility))

elif simulation_mode == "theoretical":

    for s in range(number_of_rounds_at_theoretical_simulation):
        shuffle(singles_ids)
        id_a = singles_ids[0]
        id_b = singles_ids[1]

        # make new couple
        current_couple = Couple(all_agents[id_a], all_agents[id_b])

        print("--------- Step %s\t" % s)

        while current_couple.couple_n_steps <= number_of_steps and current_couple.is_active:
            current_couple.run_step()
            current_couple.make_or_break()

        history_couples.append(current_couple)


# output

mean_utility_mat = np.zeros((n_of_types,n_of_types))
sd_utility_mat = np.zeros((n_of_types,n_of_types))
mean_morality_mat = np.zeros((n_of_types,n_of_types))
sd_morality_mat = np.zeros((n_of_types,n_of_types))
mean_n_steps_mat = np.zeros((n_of_types,n_of_types))
sd_n_steps_mat = np.zeros((n_of_types,n_of_types))

for ta in range(n_of_types):
    for tb in range(n_of_types):
        type2type_utilities = []
        type2type_moralities = []
        type2type_n_steps = []
        for hc in history_couples:
            if (hc.agent_a.moral_type == moral_type[ta] and hc.agent_b.moral_type == moral_type[tb]) or (hc.agent_b.moral_type == moral_type[ta] and hc.agent_a.moral_type == moral_type[tb]):
                type2type_utilities.append(hc.couple_average_utility)
                type2type_moralities.append(hc.couple_average_morality)
                type2type_n_steps.append(hc.couple_n_steps)

        # updating 
        mean_utility_mat[ta][tb] = np.mean(type2type_utilities)
        sd_utility_mat[ta][tb] = np.std(type2type_utilities)
        mean_morality_mat[ta][tb] = np.mean(type2type_moralities)
        sd_morality_mat[ta][tb] = np.std(type2type_moralities)
        mean_n_steps_mat[ta][tb] = np.mean(type2type_n_steps)
        sd_n_steps_mat[ta][tb] = np.std(type2type_n_steps)

# plots

min_val_colormap = -0.5
max_val_colormap = 1.5


X,Y = np.meshgrid(range(n_of_types+1),range(n_of_types+1))
ticks_pos = np.arange(0.,n_of_types+0., 1)

fig, ax = plt.subplots(2,3,figsize=(14,7))

ax = ax.flatten()

pcm0 = ax[0].pcolormesh(X,Y,mean_utility_mat, vmin=min_val_colormap, vmax=max_val_colormap)
ax[0].set_title('Couple Utility')
ax[0].set_ylabel('Mean')
ax[0].set_yticks(ticks_pos)
ax[0].set_yticklabels(moral_title, rotation=30)
ax[0].set_xticks([])

pcm1 = ax[1].pcolormesh(X,Y,mean_morality_mat, vmin=min_val_colormap, vmax=max_val_colormap)
ax[1].set_title('Couple Morality')
ax[1].set_xticks([])
ax[1].set_yticks([])

pcm2 = ax[2].pcolormesh(X,Y,mean_n_steps_mat)
ax[2].set_title('Couple N Steps')
ax[2].set_xticks([])
ax[2].set_yticks([])

pcm3 = ax[3].pcolormesh(X,Y,sd_utility_mat)
ax[3].set_ylabel('Standard Deviation')
ax[3].set_yticks(ticks_pos)
ax[3].set_yticklabels(moral_title, rotation=30)
ax[3].set_xticks(ticks_pos)
ax[3].set_xticklabels(moral_title, rotation=30)

pcm4 = ax[4].pcolormesh(X,Y,sd_morality_mat)
ax[4].set_xticks(ticks_pos)
ax[4].set_xticklabels(moral_title, rotation=30)
ax[4].set_yticks([])

pcm5 = ax[5].pcolormesh(X,Y,sd_n_steps_mat)
ax[5].set_xticks(ticks_pos)
ax[5].set_xticks(ticks_pos)
ax[5].set_xticklabels(moral_title, rotation=30)
ax[5].set_yticks([])


fig.colorbar(pcm0, ax=ax[0], orientation='vertical')
fig.colorbar(pcm1, ax=ax[1], orientation='vertical')
fig.colorbar(pcm2, ax=ax[2], orientation='vertical')
fig.colorbar(pcm3, ax=ax[3], orientation='vertical')
fig.colorbar(pcm4, ax=ax[4], orientation='vertical')
fig.colorbar(pcm5, ax=ax[5], orientation='vertical')

file_name = 'output/LoveMoralSimulation_' + str(gmtime().tm_yday) + str(gmtime().tm_hour) + str(gmtime().tm_min) + str(gmtime().tm_sec)
fig.savefig(file_name + ".png", dpi=300)
plt.show()


# print log

log_text = "simulation_mode = \"" + simulation_mode + "\"\n"
log_text += "number_of_rounds_at_theoretical_simulation = " + str(number_of_rounds_at_theoretical_simulation) + "\n"
log_text += "number_of_steps = " + str(number_of_steps) + "\n\n"

log_text += "n_agents_per_type = ("
for i in range(n_of_types):
    log_text += ( str(n_agents_per_type[i]) + ",")
log_text = log_text[:-1] + ")\n"

log_text += "moral_type = (\""
for i in range(n_of_types):
    log_text += ( str(moral_type[i]) + "\",\"")
log_text = log_text[:-2] + ")\n"

log_text += "threshold_make_break = ("
for i in range(n_of_types):
    log_text += ( str(threshold_make_break[i]) + ",")
log_text = log_text[:-1] + ")\n"

log_text += "moral_utility_factor = ("
for i in range(n_of_types):
    log_text += ( str(moral_utility_factor[i]) + ",")
log_text = log_text[:-1] + ")\n"

log_text += "moral_title = (\""
for i in range(n_of_types):
    log_text += ( str(moral_title[i]) + "\",\"")
log_text = log_text[:-2] + ")\n\n"

#log_text += "-------------------------\n\n"


with open(file_name + ".txt", "w") as text_file:
    text_file.write(log_text)
