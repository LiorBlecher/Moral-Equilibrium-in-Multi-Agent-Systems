from Agents.SMagent import SMagent
from Agents.AgentsTypes import SimpleAgent, CarefulAgent, GenerousAgent, SelfishAgent, RandomAgent, CalculatedAgent
import numpy as np
import random
from Constrains import UniConstrains


class Simulation:
    def __init__(self, id, numAgents, domainSize, connectivity):
        self.connectivity = connectivity
        self.id = id
        self.numAgents = numAgents
        self.domainSize = domainSize
        # _________________________________creations
        self.agents = {}  # { key: id, value: agent}
        self.neighbours = {}  # { key: id, value: all his neighbours}
        self.constraints = {}

# -----------------------------------------------------------------------------------create
    def create_agents(self):
        for index in range(0, self.numAgents):
            bound = round(random.uniform(0.05, 0.5), 2)
            self.agents[index] = SMagent(index, self.domainSize, bound)
        return self.agents

    def create_connections(self):
        for agent_id in self.agents.keys():
            self.neighbours[agent_id] = []
        # fully connected
        if self.connectivity <= 0:
            pass
        else:
            for agent_id in self.agents.keys():
                # how many neighbours
                mu = self.connectivity
                s = self.connectivity / 2
                num_of_neighbours = int(abs(np.random.normal(mu, s, 1)))
                # don't allow no neighbours
                if num_of_neighbours == 0:
                    num_of_neighbours = 1
                # add neighbours if...
                count = len(self.neighbours[agent_id])
                while count < num_of_neighbours:
                    potential_neighbour = random.choice(list(self.agents.keys()))
                    # if not same id - not neighbours to himself
                    if potential_neighbour != agent_id:
                        # if not already in neighbours list
                        if potential_neighbour not in self.neighbours[agent_id]:
                            self.neighbours[agent_id].append(potential_neighbour)
                            self.neighbours[potential_neighbour].append(agent_id)
                            count += 1
        return self.neighbours

    def create_constraints(self):
        for agent_id in self.agents.keys():
            constraint_per_n = {}
            neighbours = self.neighbours[agent_id]
            for neighbour in neighbours:
                con = UniConstrains(self.domainSize)
                constraint = con.create_constraint()
                constraint_per_n[neighbour] = constraint
            self.constraints[agent_id] = constraint_per_n
        return self.constraints

    # _______________________________________________________________________________________________________________
    def create_simple_agent(self):
        return SimpleAgent(0, self.domainSize)

    def create_careful_agent(self):
        return CarefulAgent(0, self.domainSize)

    def create_generous_agent(self):
        return GenerousAgent(0, self.domainSize)

    def create_selfish_agent(self):
        return SelfishAgent(0, self.domainSize)

    def create_random_agent(self):
        return RandomAgent(0, self.domainSize)

    def create_calculated_agent(self):
        return CalculatedAgent(0, self.domainSize)

