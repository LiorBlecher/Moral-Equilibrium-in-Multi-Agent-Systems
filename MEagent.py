from Agents.Agent import Agent
import math
from Messages.Message import Message


class MEagent(Agent):
    def __init__(self, id, domainSize, privacyLevel=1):
        Agent.__init__(self, id, domainSize, privacyLevel)
        self.moralEquilibrium = 0
        self.possible_ME = {}  # {key: assignment, value: ME}

    # DATA
    def get_data(self):
        # Iteration, Assignment, Utility, Moral Equilibrium
        data = [self.iteration, self.id, self.assignment, self.utility, self.moralEquilibrium, None, None]
        return data

    # _____________________________________________________________________________ALGORITHM:

    def listen(self):
        if self.phase == 1:
            self.listen_phase_1()
        elif self.phase == 2:
            self.listen_phase_2()
        elif self.phase == 3:
            self.listen_phase_3()
        elif self.phase == 4:
            self.listen_phase_4()

    def reply(self):
        if self.phase == 1:
            self.reply_phase_1()
        elif self.phase == 2:
            self.reply_phase_2()
        elif self.phase == 3:
            self.reply_phase_3()
        elif self.phase == 4:
            self.reply_phase_4()

    # ______________________________________initiate:
    def initiate(self, neighbours, constraints):
        self.init_neighbours(neighbours)
        self.init_constraints(constraints)
        self.init_domain()
        messages_to_send = self.make_value_messages()
        self.send_messages(messages_to_send)
        self.phase = 1

    # ________________________________________________________PHASE 1
    def listen_phase_1(self):
        # update local view
        for msg in self.message_box:
            self.LocalView[msg.get_sender()] = msg.get_content()  # content = neighbor's assignment
        self.clear_message_box()
        # update utility
        self.utility = self.calculate_utility(self.assignment)

    def reply_phase_1(self):
        # send preferences to all neighbors
        messages_to_send = self.make_pref_messages()
        self.send_messages(messages_to_send)
        self.phase = 2

    # ________________________________________________________PHASE 2
    def listen_phase_2(self):
        # update indications
        indications = {}
        for msg in self.message_box:
            indications[msg.get_sender()] = msg.get_content()  # content = neighbor's list pref
        self.clear_message_box()
        # look for next assignment
        self.calculate_next_assignment(indications)

    def reply_phase_2(self):
        # send social_gain and alter_value to all neighbors
        messages_to_send = self.make_alternative_value_messages()
        self.send_messages(messages_to_send)
        self.phase = 3

    # ________________________________________________________PHASE 3
    def listen_phase_3(self):
        # update alternative values
        alternative_values = {}
        for msg in self.message_box:
            alternative_values[msg.get_sender()] = msg.get_content()  # content = neighbor's alter val
        self.clear_message_box()
        # check threshold
        self.calculate_threshold(alternative_values)  # { key: neighbour_id, value: taboo}

    def reply_phase_3(self):
        # send taboo to all neighbors
        self.send_messages(self.taboos)
        self.phase = 4

    # ________________________________________________________PHASE 4
    def listen_phase_4(self):  # not monotony
        # update taboo messages
        taboos = {}
        for msg in self.message_box:
            taboos[msg.get_sender()] = msg.get_content()  # content = taboo
        self.clear_message_box()
        # check limitations
        if not taboos:  # if no taboos
            self.change_assignment()
            self.update_moral_equilibrium()

    def reply_phase_4(self):
        # send value messages
        messages_to_send = self.make_value_messages()
        self.send_messages(messages_to_send)
        # finish iteration
        self.iteration = self.iteration + 1
        self.phase = 1


    # _____________________________________________________________________________PRIVET METHODS:
    # ----------------------------calculate alter value:
    # according to my ME - Debits or Credits (Moral Compensation or Moral Licensing)
    def calculate_next_assignment(self, indications):
        beneficial_to_me, neighbours_preferences = self.divide_assignments_to_groups(indications)
        if self.moralEquilibrium >= 0:
            possible_assignment = self.strategy_moral_licensing(beneficial_to_me)
        else:
            possible_assignment = self.strategy_moral_compensation(neighbours_preferences)
        # update alter val
        self.alterValue = possible_assignment

    def divide_assignments_to_groups(self, indications):
        # for every assignment in the domain - improvement for me + local changes for neighbours
        # return two groups - beneficial to me + neighbours??? preferences
        # dictionary[assignment] = [improvement for me, local changes for neighbours]
        beneficial_to_me = {}
        neighbours_preferences = {}
        self.possible_ME = {}
        for assignment in range(self.domainSize):
            utility = self.calculate_utility(assignment)
            social_gain = 0
            for neighbour_id in self.neighbours:
                # local changes for neighbours
                indications_list_from_n = indications[neighbour_id]
                n_gain = indications_list_from_n[assignment]
                social_gain = social_gain + n_gain
            improvement_for_me = utility - self.utility
            local_changes = social_gain
            self.possible_ME[assignment] = local_changes
            # groups:
            if improvement_for_me >= 0:
                beneficial_to_me[assignment] = [improvement_for_me, local_changes]
            if local_changes >= 0:
                neighbours_preferences[assignment] = [improvement_for_me, local_changes]
        return beneficial_to_me, neighbours_preferences

    # ----------------------------calculate threshold:
    def calculate_threshold(self, alternative_values):
        # return taboo_per_n # { key: neighbour_id, value: taboo}
        start_temp = 1000
        self.taboos = {}
        for neighbour_id in alternative_values:
            perm_uti = self.only_one_change_assignment(neighbour_id)
            neighbour_alter_value = alternative_values[neighbour_id]
            constraint_matrix_with_n = self.constraints[neighbour_id]
            new_add = constraint_matrix_with_n[self.assignment][neighbour_alter_value]
            potential_utility = perm_uti + new_add
            # difference between candidate and current point evaluation
            diff = potential_utility - self.utility
            if diff < 0:
                # calculate temperature for current iteration, t->0: small percentage, t->inf:  big percentage
                temperature = start_temp - self.iteration
                # calculate metropolis acceptance criterion
                metropolis = math.exp(diff / temperature)
                # it is less likely to add taboo at the beginning of the algorithm (big temp) and if the diff is not big
                if (potential_utility/self.utility) > metropolis:
                    content = neighbour_alter_value
                    sender = self.id
                    receiver = neighbour_id
                    msg = Message(sender, receiver, content)
                    self.taboos[neighbour_id] = msg

    # PHASE 4
    def change_assignment(self):
        self.assignment = self.alterValue

    # PHASE 4
    def update_moral_equilibrium(self):
        self.moralEquilibrium += self.possible_ME[self.assignment]
